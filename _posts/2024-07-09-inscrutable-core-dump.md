---
layout: post
title: Inscrutable Coredump v. Unmoveable Grad Student
date: 2024-07-09 15:24:13-0400
description: On the applications of fuzzy human pattern matching to extract secrets from a corrupted core dump in the age of trillion parameter AI
tags:
  - gdb
categories: systems
giscus_comments: true
related_posts: false
---
Situation: we have a core dump that is shy to reveal its inner workings. The goal is to extract some more information from this core dump, using fancier analyses. The core dump is 1.2GB in size, so I know that there is some insight in there, it is just buried.

```gdb
(gdb) bt
#0  0x00007fbaa4653c30 in ?? ()
#1  0x0000000000000000 in ?? ()
```

Since we have an intact `$pc` (which refers to `%rip`), we can figure out the instructions it was executing.

```gdb
(gdb) disassemble $pc-20,$pc+20
Dump of assembler code from 0x7fbaa4653c1c to 0x7fbaa4653c44:
   0x00007fbaa4653c1c:  add    %al,(%rax)
   0x00007fbaa4653c1e:  jmp    0x7fbaa4653a51
   0x00007fbaa4653c23:  nopl   0x0(%rax,%rax,1)
   0x00007fbaa4653c28:  mov    0x98(%r12),%rax
=> 0x00007fbaa4653c30:  cmpb   $0x48,(%rax)
   0x00007fbaa4653c33:  jne    0x7fbaa4653b90
   0x00007fbaa4653c39:  movabs $0x50f0000000fc0c7,%rdx
   0x00007fbaa4653c43:  cmp    %rdx,0x1(%rax)
End of assembler dump.
```

Let us inspect the registers.

```gdb
(gdb) info reg
rax            0x323338342034342e  3617296722238387246
rbx            0x7fff678ebb50      140734930795344
rcx            0x7fba82086120      140439022231840
rdx            0x1                 1
rsi            0x1                 1
```

Okay so our `%rax` was clearly a gibberish address, no wonder dereferencing it failed. Now the question is what source file/line was mapped to `$pc`. ChatGPT says that the following can work:

```gdb
(gdb) list *$pc
<no output>
(gdb) info symbol $pc
No symbol matches $pc.
```

ChatGPT also says that we can also dereference addresses using these, but first we need to know what library is laid out in our memory, and at what offset. Noting these down for later.

```session
$ addr2line -e /path/to/your/executable 0xADDRESS
$ objdump -d -S /path/to/your/executable
```

Some more useful information, saving for later.

```gdb
(gdb) info frame 0
Stack frame at 0x7fff678ebaf8:
 rip = 0x7fbaa4653c30; saved rip = 0x0
 called by frame at 0x7fff678ebb00
 Arglist at 0x7fff678ebae8, args:
 Locals at 0x7fff678ebae8, Previous frame's sp is 0x7fff678ebaf8
 Saved registers:
  rip at 0x7fff678ebaf0
(gdb) info frame 1
Stack frame at 0x7fff678ebb00:
 rip = 0x0; saved rip = 0x0
 caller of frame at 0x7fff678ebaf8
 Arglist at 0x7fff678ebaf0, args:
 Locals at 0x7fff678ebaf0, Previous frame's sp is 0x7fff678ebb00
 Saved registers:
  rip at 0x7fff678ebaf8
(gdb) info frame 2
No frame at level 2.
```

Let's look at shared memory mappings now.

```gdb
(gdb) info shared
No shared libraries loaded at this time.
(gdb) info proc mappings
Mapped address spaces:

          Start Addr           End Addr       Size     Offset objfile
      0x5585a6034000     0x5585a604b000    0x17000        0x0 /some/bin
      0x5585a604b000     0x5585a64ef000   0x4a4000    0x17000 /some/bin
      0x5585a64ef000     0x5585a6582000    0x93000   0x4bb000 /some/bin
      0x7fba3ad28000     0x7fba3c000000  0x12d8000        0x0 /dev/shm/...
      0x7fba40d29000     0x7fba40f41000   0x218000        0x0 /dev/shm/...
```

Alright, getting somewhere. I have no idea why `info shared` failed but `info proc mappings` did not. We want to find a mapping around the address `0x00007fbaa4653c30`.

Found something.

```gdb
0x7fbaa4647000     0x7fbaa4659000    0x12000     0x3000 /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
```

The difference between the base address and our `$pc` is `0xcc30`. Add the offset `0x3000` to get `0xfc30`.

```session
$ addr2line -e /usr/lib/x86_64-linux-gnu/libgcc_s.so.1 0xfc30
??;0
```

Okay well thx.

```session
$ objdump -d -S /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
...
fc30:       80 38 48                cmpb   $0x48,(%rax)
    fc33:       0f 85 57 ff ff ff       jne    fb90 <_Unwind_GetTextRelBase@@GCC_3.0+0xe40>
    fc39:       48 ba c7 c0 0f 00 00    movabs $0x50f0000000fc0c7,%rdx
    ...
```

Okay this wasn't super useful. This is just some GCC unwinding utility function after a segfault. At this point, I just decide to examine the entire stack.

```gdb
(gdb) x/128xg 0x7fff678eba00
...
0x7fff678eba00: 0x00007fba82086040      0x00007fbaa465000b
0x7fff678eba10: 0x000000000000002e      0x0000000000000000
0x7fff678eba20: 0x0000000000000000      0x0000000000000000
0x7fff678eba30: 0x00007fff678eced8      0xb741446eb7f0e800
0x7fff678eba40: 0x00007fff678eceb0      0x00007fff678ebb50
0x7fff678eba50: 0x00007fff678ebbf8      0x00007fff678ebb50
0x7fff678eba60: 0x00007fff678ebe00      0x323338342034342d
...
```

Some patterns start to emerge. All values starting with `0x7fff` are pointers to things on the stack. Things in the range of `0x7fbaa..` are probably related to instructions. We can also see the junk value `0x3233` that was implicated in the segfault.
## Two hours later ...
My approach was to examine the stack visually, find pointers with prefixes that I knew to map to code I wore, and try and dereference them to get an idea of where my program was when it crashed.

This is doable, but it is not as straightforward as you might think. The *why* requires going into how ELF binaries/shared libraries are loaded in the memory.

1. There is a `/proc/<pid>/map` corresponding to `info proc mappings` that we saw earlier.
2. Each ELF file is divided into segments, which are further divided into sections. Mapping happens at the granularity of a segment.
3. The mapped segment will have a different offset than the on-disk segment. This may have something to do with alignment and/or ASLR requirements. But the segment sizes are also different for me, between what is reported by gdb, and what is shown by `readelf/objdump`.

As a result, I was unable to map symbol addresses from the core dump to symbols in libraries effectively. There is theoretically no reason why gdb should not be able to do this automatically, and it does, for more benign cases. But it does not seem to load the shared libraries for me for this particular crash. 

## Wait ...
Okay, I ran gdb with this specific sequence, and suddenly it chose to load shared libraries.

```gdb
$ gdb
(gdb) set auto-solib-add off # do not auto-load solibs
(gdb) set substitute-path /dev/shm /dev/null # something for shm maps
(gdb) set solib-search-path /path/to/lib
(gdb) file /path/to/my/binary
(gdb) target core /path/to/core-file
(gdb) info sharedlibrary
(gdb) info sharedlibrary
From                To                  Syms Read   Shared Object Library
0x00007fbaa4e98350  0x00007fbaa4eaccd1  No          /lib/libx.so 
0x00007fbaa4e21a00  0x00007fbaa4e72bc9  No          /lib/liby.so
...
(gdb) sharedlibrary /path/to/libmycode.so
Reading symbols from ...
```

I have no idea which of the above did the trick. Consider it a magic sequence of commands for now.

The game plan now is to go through the stack with `x/64xg $pc` and beyond to look for familiar addresses and try to resolve them via the symbol table. I tried a bunch of random symbols, and finally hit jackpot.

```gdb
(gdb) info symbol 0x00005585a6470c80
Serialize[...] in section .text of /my/binary
```
It was a buffer overflow in a serialization routine.

## Conclusions
The battle between you and a coy-acting core dump is a battle of wills. Do not blink.
