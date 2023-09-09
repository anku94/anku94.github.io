---
layout: post
title: Playing With Perf Probes
date: 2023-09-08 15:56:00-0400
description: Using perf probes for dynamic instrumentation
tags: perf
categories: systems
giscus_comments: true
related_posts: false
---

This post demonstrates the power of perf probes, using the following example C code. Let's say we'd like to verify that usleep actually sleeps for the claimed amount of time. This is the output we can get.
```
Sleep Arg: 0 us, Sleep Time: 92 us
Sleep Arg: 100 us, Sleep Time: 167 us
Sleep Arg: 200 us, Sleep Time: 262 us
Sleep Arg: 300 us, Sleep Time: 370 us
Sleep Arg: 400 us, Sleep Time: 468 us
Sleep Arg: 500 us, Sleep Time: 584 us
Sleep Arg: 600 us, Sleep Time: 684 us
Sleep Arg: 700 us, Sleep Time: 784 us
Sleep Arg: 800 us, Sleep Time: 885 us
```

Code for this exercise.

```c
#include <stdio.h>
#include <unistd.h>

int add_with_sleep(int a, int b, int sleep_us) {
  usleep(sleep_us);
  return a + b;

}

int main() {
  int ret = 0;
  for (int i = 0; i < 100; i++) {
    ret += add_with_sleep(i, i*i, i * 100);
    printf("I: %d, Ret: %d\n", i, ret);
  }

  return 0;
}
```

Series of commands. You can run them line by line.

```bash
#!/usr/bin/env bash

setup() {
  echo -1 | sudo tee /proc/sys/kernel/perf_event_paranoid
}

run() {
  gcc -g -o code code.c
  ./code

  alias perf=~/.local/bin/perf

  # -g enables call graph
  perf record -g ./code

  # DWARF enables better stack unwinding
  perf record -g --call-graph=dwarf ./code
  perf report --stdio

  # Show probe-able functions in binary
  perf probe -x ./code -F

  # Show probe-able function lines in binary
  perf probe -x ./code -L add_with_sleep

  # Show probe-able function lines in binary
  perf probe -x ./code -L add_with_sleep:2

  # Show available variables at some point
  perf probe -x ./code -V add_with_sleep:2

  # Add probes for function entry and exit. At entry, we also capture the arg.
  # If the arg is say a string, we can specify varname:string to deref the str ptr.
  sudo perf probe -x ./code --add='add_with_sleep:0 sleep_us'
  sudo perf probe -x ./code --add='add_with_sleep%return'

  sudo perf record -e probe_code:add_with_sleep -e probe_code:add_with_sleep__return ./code

  # This will generate a python script called perf-script.py
  # Modify its entry and exit functions to print deltas between
  # Entry and Exit timesteps
  perf script -g python

  sudo chown $(whoami) perf.data
  perf script -s perf-script.py | less

  ## Cleanup ##

  # Should show two events
  sudo perf probe -l
  sudo perf probe -d 'add_with_sleep'
  sudo perf probe -d 'add_with_sleep%return'
  # Should show zero events
  sudo perf probe -l


}

run
```

`perf script -g python` will generate a file that looks something like this. Incorporate these changes into the script.

```python
start = 0
start_arg = 0

def probe_code__add_with_sleep(event_name, context, common_cpu, ...):
    global start, start_arg
    start = (common_secs * 1e9) + common_nsecs
    start_arg = sleep_us

def probe_code__add_with_sleep__return(event_name, context, common_cpu ...):
    global start, start_arg
    end = (common_secs * 1e9) + common_nsecs
    time_usec = (end - start) / 1e3
    print("Sleep Arg: {:.0f} us, Sleep Time: {:.0f} us".format(start_arg, time_usec))
```

### CREDITS

1. <https://bristot.me/using-perf-probe-to-measure-execution-time-of-user-space-code-on-linux/>
2. <http://notes.secretsauce.net/notes/2019/12/16_c-probes-with-perf.html>
3. <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/monitoring_and_managing_system_status_and_performance/creating-custom-circular-buffers-to-collect-specific-data-with-perf_monitoring-and-managing-system-status-and-performance>
4. <http://blog.vmsplice.net/2011/03/how-to-use-perf-probe.html>
5. <http://oliveryang.net/2016/07/linux-perf-tools-tips/>
