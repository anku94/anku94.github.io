---
layout: post
title: Metastore Lessons for Science and Storage
date: 2026-07-05 18:46:36
description: Stealing some leaves from OLAP's playbook
tags: storage, analytics
categories: systems
giscus_comments: true
related_posts: false
ignore: false
---

This post is on the evolution of metadata and storage, weaving in PhD thesis lessons along with related trends in storage and scientific data management. While one may suspect a contribution from my new dayjob at Databricks/Unity Catalog in this zealotry, I assert an independent but concurrent lineage. I will outline the 6 trends that converge up to the moment this post unpacks:
1. Scaling debates in filesystem metadata, predominantly in HPC where we like to have 100k processes synchronously hammer our shared Lustre. Relatively outrageous solution proposals such as _no-global-namespace_^[1], along with more conventional userspace and overlay filesystems.
2. The rise of object stores^[2] and debates on whether we need a filesystem at all^[3].
3. The rise of Parquet, open table formats like Iceberg[^4] and Delta Lake^[5], and things like Liquid Clustering^[6].
4. Ankush discovering early in grad school that file formats with attributes as contiguous buffers are great for particle analytics, manifest formats describing a set of these files along with some per-file statistics, and opportunistic partial ordering run circles around almost everything^[7].
5. Ankush discovering that telemetry persisted as JSON or CSV is one of the leading causes for global suffering among those trying to understand and fix their systems^[8], and that things go much faster once you use this Pandas format called _feather_.
6. Ankush finally embracing the daylight and building a system for trace-event analytics around in-situ dataframe analytics and timestep-partitioned Parquet. Missing a manifest format that would just bundle everything together, and learning about Iceberg/Delta Lake (DL) as the paper is being wrapped up^[9].

I will now stop referring to myself in third-person. Ok, we get it: columnar analytics is great. For enterprise data, particle data, even trace data. But this is 2026, we know this, and it is not exactly the second coming of Yahoo Messenger. But this becomes the backdrop against which we evaluate how a filesystem and metadata should and can look like.

Before I go deeper into metadata, let me emphasize that columnar analytics seems to me to be more general than you might think. The world of scientific computing is packed with oddball use-cases that OLAP would not have encountered: N-D arrays, HDF5, irregular meshes etc being some of them. But it turns out that HDF5 is just contiguous buffers and pointers. Your data structure might be 3D but your memory is not, and we really only get to preserve one dimension. Do we really need multiple container formats for contiguous buffers? How far does the dominion of columnar analytics formats really extend? A frontier, if one exists, is beyond my line of sight.

With that, let us now get to metadata. In the face of the rising tide of object stores, I have argued that you cannot just have your storage system be a zillion objects. One day you are going to ask: who do these zillion objects belong to and can I delete them? An instructive lesson from politics is that when people act irrationally, it is not sufficient to critique irrational behavior---however gratifying it might be. The rational side must reflect on why it lost some customers. This is obviously directed at POSIX.

When 100,000 ranks rise in harmony and hammer their filesystems with bits, they are not publishing relevant facts in the moment. It is only when the storage phase, orchestrated by a lead rank, wraps up that a publishable entity emerges---an analytical dataset. It is fruitless to create durable metadata from 100,000 ranks synchronously. The objects must be allowed to be written without filesystem interference and then committed atomically via a manifest file (or hierarchies thereof) by the lead rank. Hierarchical in-fabric aggregation is how anything scales in a supercomputer. We just never extended this principle to storage. The commit artifact---the manifest---not only tells you about the existence and the location of its constituent objects, but it also contains indices and statistics that can enable query planning and optimization and pruning. Now _this_ is metadata, and POSIX never stood a chance.

The other oddity database folks conjured up and I just learned about is a _Metastore_. To me, it seems to be their take on a filesystem, with catalogs and schemas and tables. Now there are plenty of SQL tables in the world and a namespace to manage them seems natural, and if metastores were everything, DBFS would not be a thing... but it does play a role in the data management lifecycle in the Iceberg world by facilitating atomic commits of Iceberg/DL updates. HPC does not really need metastores, I suppose, if you do not require your Iceberg/DL metadata to span filesystem boundaries you can achieve the same outcome with a single Lustre instance.

One must give this to databases: they evolved principled definitions of consistency and isolation semantics, and you inherit these properties if you build your namespaces on top of these tools. Metastores share these characteristics, and as a result you get a richer description of your world that allows more applications to do more things. But the road to this heaven is gatekept by Codd and schemas and constraints are the toll one must pay to enter. For when they commit the sin of bearing digital contraband of uncertain structure and provenance, heathens will always find refuge in a filesystem.

My pitch for HPC, to be clear, is checkpointing as a commit protocol, with ranks writing portions of a dataset independently, and generation of a manifest describing these portions orchestrated by a multi-tier reduction hierarchy. The root of this reduction hierarchy commits the epoch to the filesystem after all objects are in. These catalog and container formats are common and interoperable, with former not only enumerating/locating the latter, but also indexing statistics for analytics.  In addition to facilitating the commit, the reduction hierarchy also enables streaming reorganization and in-situ analytics/filtering/aggregation before any bit hits a durable layer. Take-home question: _what does a scientific catalog look like?_

**Aside: MapReduce > SQL**.  I suppose there was no reason to go down this route, but reason is not why this blog exists.  Some flavor of MapReduce seems to me to the best version of general-purpose analytics, and also more applicable to scientific analytics than we might think. MapReduce is the best runtime for OLAP because it is more general than SQL, but not terribly more complex. ChatGPT says that Stonebraker said something around this and that it might be wrong. I do not trust ChatGPT. Anyway, beyond a shuffler, all SQL operators are just different flavors of map functions that you can reason about a bit for optimization. Note that MapReduce does not necessarily mean Spark: the multi-tier columnar reduction and in-situ analysis framework described above is coming with [9].

**References**
[^1]:  DeltaFS: A scalable no-ground-truth filesystem for massively-parallel computing, _Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis_, https://dl.acm.org/doi/10.1145/3458817.3476148
[^2]: DAOS: A Scale-Out High Performance Storage Stack for Storage Class Memory, _Supercomputing Frontiers_, 
[^3]: https://blog.glennklockwood.com/2025/02/llm-training-without-parallel-file.html 
[^4]: Apache Iceberg - Apache Iceberg™,https://iceberg.apache.org/
[%5]: Delta lake: High-performance ACID table storage over cloud object stores, _Proceedings of the VLDB Endowment_, https://dl.acm.org/doi/10.14778/3415478.3415560
[^6]: Liquid Clustering: https://delta.io/blog/liquid-clustering/
[&7]: CARP: Range Query-Optimized Indexing for Streaming Data, _SC24: International Conference for High Performance Computing, Networking, Storage and Analysis_, https://ieeexplore.ieee.org/document/10793150
[*8]: Lessons from Profiling and Optimizing Placement in AMR Codes, _2025 IEEE International Conference on Cluster Computing (CLUSTER)_, 
[^9]: ORCA: Steerable Observability for Bulk-Synchronous Parallel Applications, _The international conference for high performance computing, networking, storage, and analysis_ (to appear)