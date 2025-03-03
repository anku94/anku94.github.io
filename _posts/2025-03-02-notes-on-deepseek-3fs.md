---
layout: post
title: Notes on Deepseek 3FS Filesystem
date: 2025-03-02 14:19:21
description: Notes on the Fire-Flyer Filesystem by Deepseek
tags:
  - filesystems
  - storage
categories: systems
giscus_comments: true
related_posts: false
ignore: false
---
This is just me making some quick notes on the 3FS Parallel Filesystem from Deepseek. Caveat that while I have opinions on all systems, filesystems is strictly not my day job and I have to go back and think about a bunch of things and it doesn't quite work, and this post will likely have a bunch of mistakes.
# Services in 3FS
- Cluster manager: highly available, manages membership, config etc (uses zookeeper?)
- Metadata service: uses FoundationDB
- Storage service (chunk store?)
- Client (two implementations: FUSE-based, and a more performant one.)
# Metadata in 3FS

### The Ongoing Metadata Debate

Whether we need object stores or filesystem semantics has been a topic of conversation recently. My own views so far:

- I buy the argument that data accesses during a training run do not need a namespace. Maybe the namespace can be _batch-updated_ later on, if it gets in the way and does not provide the required performance.
- I feel that the usability argument still applies. At some point, you need to think about what does all the data mean, what to keep around, what to prune. There are a million reasons -- legal, regulatory, financial, just basic IT maintenance that require metadata. Long-term, it is easy to think about things as a group or a hierarchy.

I think performant fileystem namespaces is doable. It may get needlessly hard if you tie yourself to a spec or a standard. That is because this is in flux, and we do not yet have unanimous agreement on what the standard should look like.
### The 3FS Approach

They use a key-value model for their metadata, built on top of FoundationDB. Each key represents an inode.

FoundationDB, as an aside, is a very interesting database. It is like a distributed RocksDB with support for strict serializability in transactions. This is interesting to me --- normally you think of KV stores as single-node storage backends for DBMSes to use. Transactions are implemented at a SQL level. FDB implements transactions at the KV level, but is supposed to be a lower-level database you layer on top of. (Aside: I wonder what the end-to-end principle says about the correct layering). It is like a persistent distributed software transactional memory, that tries to be lock-free, with optimistic and multi-version concurrency control.

- File inodes are `INOD<inode_id>`, mapped to ownership, permissions, times., and chunk information etc. for files. Interestingly, they encode `inode_id` in little-endian to spread inodes across FDB nodes. Directory inodes begin with `DENT`, have bidirectional links to parents to ensure no loops.needs to be and should be super-fast.
- `fstat`, `lookup`, `listdir` etc. invoke read-only txns. `crate`, `link` etc. invoke read-write txns.

### State in 3FS

3FS metadata stores are stateless. Any operation is a self-contained transaction.

The metadata service does store file descriptors for files opened in write mode, but not in read mode. This helps with bootstrapping training jobs. This IMO is super important!! Any parallel job, when bootstrapping, needs to retrieve a large number of files in read-only mode. This should be super-fast, but is not so with Lustre. I vaguely recall someone mentioning that they had to hack on a cache on top of Lustre to push `.so` libraries to MPI ranks, and thinking that this feels like a fundamental flaw in what is supposed to be a parallel filesystem.

Question: how do you handle a write request for a file that is currently open in read-only mode? Ideally you need to track the readers and revoke their lease, but that requires maintaining state at the metadata layer? I think that's done by tracking versions?
## Chunk Store

This is relatively straightforward. It is per-node, and comes with a RocksDB instance for chunk metadata. Chunk metadata is cached in-memory. They have 11 chunk sizes from 64 KiB to 64 MiB. I don't think this is a big deal but metadata shouldn't be too much, even with 64KiB chunks, it is a little surprising that they went for this number of chunk sizes. But eh. Updates are CoW -- old chunks remain valid until update completes.
## Chain Replication

They use CRAQ (Chained Replication with Apportioned Queries) for replication. This is just a fancy way of saying that any replica can respond to a read request, with the catch being that you may get a stale version. A node may have a committed version of a block and a pending version. If so, it lets the requester know the existence of both versions, and the decision on whether to tolerate staleness or try again is left to the requester. Note that this is different from the case where a chain replica does not even know of the existence of an update -- I don't know if stale reads are tolerated in that case (or maybe version numbers are used to read a consistent snapshot).
## Zero-copy in FUSE!?

They use FUSE for clients, so as to not deal with debugging kernel panics. They define an interface called `USRBIO`, for zero-copy interaction between the userspace and the FUSE layer. `USRBIO` is inspired by `io-uring` (or the Verbs API for that matter). The FUSE process manages Verbs-registered memory and submission/completion rings, and does the dispatch etc. These zero-copy ops are only used for the data path, and metadata ops still go through regular FUSE APIs.
## Misc

- Codebase is mostly C++ with some Rust.
- They use `P` to verify their protocols. `P` is apparently a formal verification language for event-driven distributed services. Very cool!
- They seem to use `flatbuffers` for serdes and their own RDMA/RPC wrappers on top of the `verbs` interface. There's a lot of code there and I just briefly skimmed through it.
- They heavily use `folly`, Facebook's assorted library of C++ abstractions (including coroutines).

# Epilogue

Not sure what to make of this. Writing a parallel filesystem is a massive undertaking. While metadata bottlenecks is a well-known problem in parallel filesystems, offloading it entirely to a DB like FoundationDB is an interesting choice. I have been trying to revisit how Colossus/Tectonic manage their metadata, and it is Bigtable and ZippyDB respectively. Ceph is pretty much the only open-source filesystem to support multiple metadata servers (Lustre is unwieldy in multiple ways). 3FS is optimized for RDMA fabrics over the data path, and makes subtle choices (like cheap metadata reads) to optimize for a large parallel job bootstrapping. I remember reading somewhere that it is designed for small random accesses, and I don't really see why that is the case. I will end with the caveat that there are a lot of things to keep straight in distributed/parallel filesystem discussions, I don't really work on these, and this post probably has a bunch of mistakes.

(Oh their design notes do say that they enable random access to training samples, I don't see how they optimize for random accesses, maybe they mean that their system will transfer partial chunks and not do aggressive prefetching etc?)
# References
[^1]: https://github.com/deepseek-ai/3FS
[^2]: https://github.com/p-org/P