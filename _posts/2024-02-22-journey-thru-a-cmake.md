---
layout: post
title: Journey Through A CMake Dependency Problem
date: 2024-02-22 15:17:06-0500
description: Or how to craft artisan ELF files with exquisitely detailed metadata
tags: systems, cmake
categories: systems
giscus_comments: true
related_posts: false
---

Situation: I have a CMake project that needs `libfabric`, which needs `rdma-core`.

Both of these are non-CMake Projects, but they generate `pkg-config` files in `/prefix/lib/pkg-config`.

**Q. How to locate these libraries as dependencies in my CMake project?**

A. Use CMake's `PkgConfig` package.

```CMake
find_package(PkgConfig)
pkg_check_modules(LIBFABRIC REQUIRED IMPORTED_TARGET GLOBAL libfabric>=1.14)

if (LIBFABRIC_FOUND)
  message(STATUS "LIBFABRIC_INCLUDE_DIRS: ${LIBFABRIC_INCLUDE_DIRS}")
  message(STATUS "LIBFABRIC_LIBRARY_DIRS: ${LIBFABRIC_LIBRARY_DIRS}")
else()
  message(FATAL_ERROR "LIBFABRIC not found.")
endif()

target_link_libraries(exec PRIVATE PkgConfig::LIBFABRIC)
# Side note: I don't know what GLOBAL does
# I thought it'd get the target out of the pkg-config namespace. Apparently not.
```

**Q. Ok, code was built, but it can not locate libraries at the custom path.**

A. You could use `LD_LIBRARY_PATH`, but that's honestly annoying. With `RPATH/RUNPATH`, your binary knows where to find the packages it was linked to.

```
$ ldd exec
        linux-vdso.so.1 (0x00007ffe733f7000)
        libfabric.so.1 => /opt/fi_bench/libfabric/fab-prefix/lib/libfabric.so.1 (0x00007ff4d8924000)
        libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007ff4d873b000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007ff4d8720000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007ff4d852e000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007ff4d8526000)
        librdmacm.so.1 => not found
        libibverbs.so.1 => not found
        libnuma.so.1 => /lib/x86_64-linux-gnu/libnuma.so.1 (0x00007ff4d8519000)
        librt.so.1 => /lib/x86_64-linux-gnu/librt.so.1 (0x00007ff4d850e000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007ff4d84eb000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007ff4d839a000)
        /lib64/ld-linux-x86-64.so.2 (0x00007ff4d92ea000)
```

Why can it not find `librdmacm.so.1` or `libibverbs.so.1`? We run `make VERBOSE=1` to intercept the compile command.

```bash
/usr/bin/c++ -Wl,-rpath,/opt/fi_bench/libfabric/rdma-core-50.0/build/lib CMakeFiles/server.dir/server_main.cpp.o CMakeFiles/server.dir/common.cc.o CMakeFiles/server.dir/fabric.cpp.o CMakeFiles/server.dir/endpoint.cpp.o CMakeFiles/server.dir/benchmark.cpp.o -o server  -Wl,-rpath,/opt/fi_bench/libfabric/fab-prefix/lib:/opt/fi_bench/libfabric/rdma-core-50.0/build/lib /opt/fi_bench/libfabric/fab-prefix/lib/libfabric.so /opt/fi_bench/libfabric/rdma-core-50.0/build/lib/libibverbs.so
```
We see that the build process is supplying the relevant rpaths. Why are they not being resolved?

```
$ readelf -d executable | head

Dynamic section at offset 0x5c60 contains 31 entries:
  Tag        Type                         Name/Value
 0x0000000000000001 (NEEDED)             Shared library: [libfabric.so.1]
 0x0000000000000001 (NEEDED)             Shared library: [libstdc++.so.6]
 0x0000000000000001 (NEEDED)             Shared library: [libgcc_s.so.1]
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
 0x000000000000001d (RUNPATH)            Library runpath: [/opt/fi_bench/libfabric/rdma-core-50.0/build/lib:/opt/fi_bench/libfabric/fab-prefix/lib:/opt/fi_bench/libfabric/rdma-core-50.0/build/lib]
```

So apparently `server` does not have `libibverbs.so` as a dependency! So it doesn't care about its rpath. It must be coming from `libfabric.so` then.

```
$ ldd libfabric.so.1
        librdmacm.so.1 => not found
        libibverbs.so.1 => not found
        libnuma.so.1 => /lib/x86_64-linux-gnu/libnuma.so.1 (0x00007f534861b000)
        librt.so.1 => /lib/x86_64-linux-gnu/librt.so.1 (0x00007f5348610000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f53485ed000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f53485e5000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f53483f3000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f5348fee000)
```

Why does `libfabric` not preserve rpaths?

At this point I don't care. I just hacked the rpaths into LDFLAGS.

```
$ verbs_PREFIX=$RDMA_PATH/build verbs_LIBDIR=$RDMA_PATH/build/lib LDFLAGS="-Wl,-rpath,$RDMA_PATH/build/lib" ./configure --prefix=/opt/fi_bench/libfabric/fab-prefix
```

Afterwards,

```
$ ldd libfabric.so
        linux-vdso.so.1 (0x00007ffecb1d0000)
        /users/ankushj/repos/stderred/build/libstderred.so (0x00007f9e73c24000)
        librdmacm.so.1 => /opt/fi_bench/libfabric/rdma-core-50.0/build/lib/librdmacm.so.1 (0x00007f9e73c07000)
        libibverbs.so.1 => /opt/fi_bench/libfabric/rdma-core-50.0/build/lib/libibverbs.so.1 (0x00007f9e73be5000)
        libnuma.so.1 => /lib/x86_64-linux-gnu/libnuma.so.1 (0x00007f9e73bd0000)
        librt.so.1 => /lib/x86_64-linux-gnu/librt.so.1 (0x00007f9e73bc5000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f9e73ba2000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f9e73b9a000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f9e739a8000)
        libnl-3.so.200 => /lib/x86_64-linux-gnu/libnl-3.so.200 (0x00007f9e73985000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f9e745e2000)
        libnl-route-3.so.200 => /lib/x86_64-linux-gnu/libnl-route-3.so.200 (0x00007f9e7390b000)
```

You can love systems, rarely do they love you back.
