---
layout: post
title: On Filesystems vs Object Stores
date: 2025-02-17 10:07:40
description: Some description
tags:
  - tag
categories: cat
giscus_comments: true
related_posts: false
ignore: false
---
Quick notes on the debate.

Bottleneck is the directory inode.

You create a million objects and then you need to file them.

File them async.

Full POSIX makes this complicated.

Idea: you start with a metadata layer that only allows read-only views over a large object store.

Usability tradeoff. So for a batch parallel job, you want it to do its object store business independently, and then generate diffs to be appended to the filesystem async.

Serialize per-job rather than per-file.

## References
[^1]: https://blog.glennklockwood.com/2025/02/llm-training-without-parallel-file.html
[^2]: ABC