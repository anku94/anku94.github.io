---
layout: post
title: Using perf probes to intercept variables
date: 2024-05-29 18:12:07-0400
description: Intercept process variables without having to modify it
tags:
  - perf
categories: perf
giscus_comments: true
related_posts: false
---
[Part 1]() and [Part 2]() of this series at the respective links.

This is a case study in using perf probes to monitor the values of some variable from a process, without having to modify its code.

We are interested in monitoring the number of objects allocated by a library called `psm`. We know that they are available in a function called `psm_mpool_get`. The object available there is called `mp` and it has members `mp_num_obj` and `mp_num_obj_inuse` that we want to monitor.

First, set up your permissions.

```bash
#!/bin/bash
sudo addgroup tracing
sudo usermod -aG ankush tracing
newgrp tracing # "activate" group without having to log out
sudo mount -o remount,mode=755 /sys/kernel/debug
sudo mount -o remount,mode=755 /sys/kernel/debug/tracing
echo 0 | sudo tee /proc/sys/kernel/kptr_restrict
echo -1 | sudo tee /proc/sys/kernel/perf_event_paranoid
sudo chown root:tracing /sys/kernel/debug/tracing/uprobe_events
sudo chmod g+rw /sys/kernel/debug/tracing/uprobe_events
```

Next, we execute these commands to explore the available perf points and tap into them

```bash
PSM=/path/to/libpsm_infinipath.so

perf probe -x $PSM --funcs # lists probe-able functions
perf probe -x $PSM --funcs | grep psmi_mpool_get # this is present
perf probe -x $PSM -L psmi_mpool_get # view the source for this function
perf probe -x $PSM --vars psmi_mpool_get # view available vars here.

# mp is available in psmi_mpool_get

# need mp->mp_num_obj and mp->mp_num_obj_inuse
perf probe -x $PSM 'psm:nobj=psmi_mpool_get mp->mp_num_obj'
perf probe -x $PSM 'psm:nused=psmi_mpool_get mp->mp_num_obj_inuse'
```

List active probes to confirm that they got added

```
$ perf probe -l
  psm:nobj             (on psmi_mpool_get@src/psm/psm_mpool.c in ...>
  psm:nused            (on psmi_mpool_get@src/psm/psm_mpool.c in ...>
```

Start recording for all probes.

```bash
perf record -e psm:nobj -e psm:nused -a
# run code from a different tab
^C
perf script # this will show us what was emitted
```

Output:

```
 bin-using-psm 381026 [002] 417634.233519: psm:nused: (7f9980230350) mp_num_obj_inuse=0x0
 bin-using-psm 381027 [003] 417634.233519: psm:nused: (7fcc080f5350) mp_num_obj_inuse=0x0
 bin-using-psm 381028 [004] 417634.233519: psm:nused: (7fc05836e350) mp_num_obj_inuse=0x0
 bin-using-psm 381027 [003] 417634.233522:  psm:nobj: (7fcc080f5350) mp_num_obj=0x400
 bin-using-psm 381028 [004] 417634.233522:  psm:nobj: (7fc05836e350) mp_num_obj=0x400
 bin-using-psm 381026 [002] 417634.233522:  psm:nobj: (7f9980230350) mp_num_obj=0x400
 bin-using-psm 381029 [005] 417634.233523: psm:nused: (7fa818f52350) mp_num_obj_inuse=0x0
 bin-using-psm 381029 [005] 417634.233525:  psm:nobj: (7fa818f52350) mp_num_obj=0x400
 bin-using-psm 381030 [006] 417634.233525: psm:nused: (7f69a6c35350) mp_num_obj_inuse=0x0
 bin-using-psm 381030 [006] 417634.233527:  psm:nobj: (7f69a6c35350) mp_num_obj=0x400
```

Bingo --- we have the data. Other things:

1. We can point `perf record` to a particular PID to record its values.
2. We can process the data via say python using `perf script -g python`

### References
[1]: https://manpages.ubuntu.com/manpages/noble/en/man1/perf-probe.1.html