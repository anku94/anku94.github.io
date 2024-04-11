---
layout: post
title: Replication Part 1 - Primary-Backup vs Chain Replication
date: 2024-04-11 13:35:30-0400
description: Simplifying scheme soup with successive steps
tags: 
categories: systems
giscus_comments: true
related_posts: false
---
The purpose with this series of posts, to the extent it is followed through, is to arrive at different replication schemes by applying diffs to some well-understood schemes. This exercise should help us understand the tradeoffs, the design space, and reason about whether a point in the design space is pareto-optimal, that is, can its pros be realized by a diff over some other design point with less cons.

This is somewhat facetious, but IMO there are two classes of people in the distributed systems world — Leslie Lamport, who stared into the soul of replication and figured out something fundamental a couple of decades ago and has since been trying to tell us all that everything in replication is a specialization of that [principle][1,2,3], and everyone else.

Part 1 will cover 3 basic designs. For now, we will assume single-key operations and key-value semantics, and see how far this simple model gets us.

Let me also try to assign relative perf numbers for these, where 100 is the max perf for a single-node design (writes and reads are assumed to be symmetric cost-wise, so a 100 perf for writes and reads just means that any combination of the two will have a perf of 100. Perf = latency = throughput as we can assume one request in flight at a time, WLOG?). So a perf of 500 implies 5X the read throughput of a single node.
##### 1. A Single Worker

(Worker could be a core, or a node, or a datacenter even. We relax consistency for performance all the way down.)

Design: a single worker, receives all requests, applies them sequentially, writes see reads, works great, no issues.

Consistency: Strict
Failure: No tolerance
Read Perf: 100
Write Perf: 100
##### 2. Primary-Backup

Two workers. All requests are handled by the primary. All writes are synchronously copied to backup. Backup kicks in on failure.

Consistency: Strict
Failure: Tolerates 1
Read Perf: 100
Write Perf: 50 (assuming synchronous copying = as costly as query)
##### 2a. Primary-Backup with Async Replication

Primary can ACK to a request before replication to backup is completed. It is a meaningless design point because async replication has no tolerance for failures. The delta between the two can be lost.
##### 2b. Primary-Backup with Backup Serving Reads

The backup is right there, and it is idle. Can we use it?

We won't use it for writes, because concurrent writes to the same key can cause conflicts and we do not yet know how to resolve them. Also we have not evolved and coordination mechanism yet. But we could use it for reads... right?

But it should respond to reads without requiring coordination with the primary, otherwise we have not really gained anything in terms of performance. But that has consistency implications — what if the primary is concurrently updating the value we returned?

This works under two cases:

1. A looser consistency model, Sequential Consistency, is acceptable, OR
2. The Primary and Backup can establish a coordination mechanism that is more efficient than what the clients can do (sharding keys is one example of such a mechanism)

For case 2b1.

Consistency: Sequential
Failure: Tolerates 1
Read Perf: 200
Write Perf: 50
##### 3. Chain Replication

Chain Replication is just a generalization of 2b. Instead of having one replica,  you can have N replicas. In fact, for 1:N primary-read serving backup systems, I think these two are logically equivalent:

1. The primary chaining writes sequentially through replicas
2. The primary broadcasting writes to all replicas

First option increases latency by N, and the second option requires the primary to do $N\times$ more communication.

I think the two only have perf implications, but are logically equivalent to each other and to 2b.
#### References

[1]: The part-time parliament, ACM Transactions on Computer Systems, Leslie Lamport
[2]: Paxos Made Simple, ACM SIGACT News, Leslie Lamport
[3]: Vertical paxos and primary-backup replication, Proceedings of the 28th ACM symposium on Principles of distributed computing, Leslie Lamport, Dahlia Malkhi, Lidong Zhou
