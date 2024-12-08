---
layout: post
title: An Exercise in Debugging When the Kernel Is Implicated
date: 2024-04-15 16:22:10-0400
description: The problem here was being caused by a kernel module misbehaving because a remote service was misbehaving.
tags:
  - "#systems"
  - "#gdb"
categories: debugging
giscus_comments: true
related_posts: false
---
Situation: an MPI application (10s of processes) seems to freeze after completion. Once it freezes, I can't attach to any of its processes via `gdb -p` (that also freezes). I can't `SIGTERM` or even `SIGKILL` the processes. `ps aux` (my standard set of ps flags) shows the processes in either an `Is` state, or a `Ds` state.

Apparently, `D` processes are waiting for I/O in a non-interruptible state. `I` processes are idle, and are in an interruptible state. If I tried to poke around in `/proc/<pid>` too much, even procfs would freeze.

## wchan

The first useful thing I learned was the `wchan` column in `ps`. `wchan` means wait channel - it tells you what stream (or whatever the definition of a channel is) is a process waiting on.

```
$ -eo ppid,pid,user,stat,pcpu,comm,wchan -p 21061 | grep stoch
  21028   21060 ankushj  Zs    0.3 stoch <defunct> -
  21028   21061 ankushj  Is    0.4 stochastic_subg ptlrpc_set_wait
  21028   21062 ankushj  Zs    0.2 stoch <defunct> -
  21028   21068 ankushj  Zs    0.2 stoch <defunct> -
  21028   21069 ankushj  Ds    0.4 stochastic_subg rwsem_down_write_slowpath
  21028   21070 ankushj  Ds    0.4 stochastic_subg rwsem_down_write_slowpath
  21028   21071 ankushj  Zs    0.4 stoch <defunct> -
  21028   21072 ankushj  Zs    0.4 stoch <defunct> -
  ...
```

Bingo - we have some function names to blame. Apparently we can get more context around these without needing to attach a debugger, which we can not.

We can `cat` `/proc/<pid>/stack` to get a stack trace from a process without a debugger. Thankfully this works.

```
$ sudo cat /proc/21061/stack

[<0>] ptlrpc_set_wait+0x5e8/0x730 [ptlrpc]
[<0>] ptlrpc_queue_wait+0x88/0x230 [ptlrpc]
[<0>] ldlm_cli_enqueue+0x436/0x990 [ptlrpc]
[<0>] mdc_enqueue_base+0x2f2/0x1c90 [mdc]
[<0>] mdc_intent_lock+0x212/0x530 [mdc]
[<0>] lmv_intent_lock+0x385/0x16b0 [lmv]
[<0>] ll_lookup_it+0x7ad/0x20e0 [lustre]
[<0>] ll_atomic_open+0x198/0xff0 [lustre]
[<0>] lookup_open+0x364/0x6e0
[<0>] do_last+0x2cb/0x900
[<0>] path_openat+0x8d/0x290
[<0>] do_filp_open+0x91/0x100
[<0>] do_sys_open+0x17e/0x290
[<0>] __x64_sys_openat+0x20/0x30
[<0>] do_syscall_64+0x57/0x190
[<0>] entry_SYSCALL_64_after_hwframe+0x44/0xa9
```

```
$ sudo cat /proc/21065/stack

[<0>] rwsem_down_write_slowpath+0x244/0x4d0
[<0>] do_last+0x2b1/0x900
[<0>] path_openat+0x8d/0x290
[<0>] do_filp_open+0x91/0x100
[<0>] do_sys_open+0x17e/0x290
[<0>] __x64_sys_openat+0x20/0x30
[<0>] do_syscall_64+0x57/0x190
[<0>] entry_SYSCALL_64_after_hwframe+0x44/0xa9
```

This is beautiful! Instead of gaslighting ourselves and slipping into an existential crisis, we can point our fingers elsewhere.

## Conclusion

Both these stack traces indicate getting stuck on a File I/O call. The first trace is more specific - it tells us that it is a Lustre I/O. Lustre is a parallel filesystem.

Turns out that one of my Lustre OSTs was dead. That would explain this behavior - the Lustre module sits in the kernel, and is blocked trying to reach that OST. Maybe there are good reasons a timeout there can not be handled gracefully, maybe there are not. But a kernel module freezing is tough - a whole bunch of debugging options go for a toss. Thankfully some still work!