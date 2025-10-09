---
layout: post
title: Is RDMA Misunderstood?
date: 2025-10-06 14:51:13
description: Do we keep doing repeating certain things in academic work on HPC fabrics?
tags: infiniband
categories: systems
giscus_comments: true
related_posts: false
ignore: false
---

In this post, I explore the thesis that we keep redoing certain things in fabric design because the history is not properly documented. It is an ambitious claim, and the understanding I need to build to make it comprehensively and conclusively remains elusive, and this is an attempt at a sloppier fail-fast version. Let me reiterate the _fail-fast_ bit: this post was written with an appetite for my own hat. It also forms a loose series with [this](https://ankushja.in/blog/2023/infiniband-flavors/), [this](https://ankushja.in/blog/2024/network-tradeoffs/), and [this](https://ankushja.in/blog/2024/credits-flow-congestion/).

Edit: _I prompt-engineered some LLMs into generating [this](https://users.ece.cmu.edu/~ankushj/cbfc.pdf). Same reliability caveats as the rest of the post apply._

## Losslessless: The Bedrock of RDMA

RDMA originated on a natively lossless fabric (Infiniband). Since then, we have tried to graft it into inherently lossy fabrics, with brittle outcomes. We like losslessness for the same reason we like strong consistency: it is nice and simple if things just work and are predictable.

1. Every network becomes lossless at low utilization.
2. CBFC is the best way we know to build a lossless network at higher traffic volumes. PFC is very fragile, intrinsically so.
3. CBFC and PFC represent two fundamentally differing approaches to utilization management: proactive and reactive, with their own tradeoffs. The cost of a proactive approach is _"imposing flow control when it was unnecessary"_, leading to potential underutilization.
4. There is a fundamental tradeoff between network utilization and loss guarantees. For any given lossless network, you can afford to be a little speculative and increase median usage. The null hypothesis is that this increases loss probability. Unless reasoned all the way through and demonstrated to not exist or not be a factor, it must exist.
5. We like lossless networks because in certain conditions, the cost of loss to higher layers is prohibitive. We should not design lossless schemes that dispatch speculatively without reasoning about why we wanted a lossless scheme in the first place, and why that speculative dispatch does not create problems we wanted to avoid[^2].

## Everyone Likes Most of Infiniband

Let us disaggregate infiniband into a series of features.

Likes:
1. Everyone likes CBFC[^1,2,3]
2. Everyone likes the performance benefits of RDMA, if not the complexity of memory registration and coding verbs.

Dislikes:
1. Everyone dislikes its difficult relationship with the broader datacenter network. It is not a part of the broader network, but a separate sub-network like NVLink or CXL.
2. Many folks dislike its scalability constraints (connections need QPs need NIC SRAM).

## What We Really Need: RD + Ethernet Compatibility

### Case Study: QLogic

QLogic already had this insight 15 years [ago](https://www.youtube.com/watch?v=E0uSl_gyZnI). QLogic is not super well known, and I think it is unfortunate. Many aspects of their approach are highly relevant to some debates we have had since.

QLogic Truescale was the precursor to Intel Omnipath, which was the precursor to Cornelis Networks. Instead of offload to a smart NIC, they wanted _onload_: CPU-mediated communication for scalability. It was a verbs-compliant fabric that natively spoke a different interface called [psm](https://github.com/pdlfs/psm).

Truescale was a messaging-oriented fabric. I think of it as RDMA UD with large datagram sizes. It injected small payloads inline into a packet, and large payloads were DMA'ed on both the send and receive paths using transient connection mechanisms called TID/TIDflows.

From what I understand, PSM had CBFC but no _link-level retry_ (LLR). It had a software-based go-back-N-style recovery. I think link-level retry requires a smarter HCA, which they were trying to avoid, at least for the first generation. I have observed software-based retries in that fabric to add an extraordinary amount of jitter, when triggered, but it is triggered by some residual bugs and high timeouts, and not by packet drops.

### Case Study: SRD in Amazon EFA

The variable-sized datagram design point remains compelling. Amazon built a fabric called _Elastic Fabric Adapter (EFA)_ that presumably adds LLR to UD. I don't know much about it so I'll keep it short.

## RDMA vs RPCs: A False Dichotomy?

I'm probably wading into a decade-old debate at this point, but it's not my fault that I was just a swaddling infant a decade ago.

Let us take eRPC[^1], an iconic paper at this point. The argument I will explore is whether eRPC implements Infiniband in software over lossy ethernet, and whether while a solid step forward for lossy ethernet, its design just strengthens the argument for _real RDMA/infiniband_.

1. eRPC likes losslessness. They create those conditions by having session credits and limiting dispatched traffic to network BDP. Session credits resemble an end-to-end version of CBFC, something also tried in [^3].
2. eRPC likes contiguous message buffers, an event loop for short messages, and memcpy'ed contiguous buffers for large messages, with memcpy orchestrated by CPU. This feels very close to the workflow I employ in my current codebase using the RDMA-capable Mercury RPC library, except using CPU cycles instead of RDMA.

I wonder what is the difference between "_we found a lossless regime in the network and designed a system optimized for a lossless common-case_" and "_we engineered a lossless regime in the network, and this proves the value of a genuinely lossless fabric._"

I also wonder about the value of pushing retries to the application layer when the ultimate behavior you want is lossless. There are plenty of applications that tolerate lossiness end-to-end, and it makes sense for the lowest common denominator to not include retries for general-purpose networks. But datacenters are a controlled high-density environment, and maybe it is easier to permit lossy flows as a second-class citizen in a lossless fabric than the other way round?

Also, I think scalability criticisms of infiniband are hardly the killer argument they are made out to be. Truescale is an example of a production fabric that already solved those challenges, and software-level solutions such as `RxD` exist in libfabric (multiplexing RDMA over UD). RDMA is not infiniband, and there are multiple CBFC-based approaches to lossless fabrics.

Next, I think RDMA doesn't preclude the ability to do two-sided communication. I think it is not completely accurate to think of RDMA as disaggregated memory. That is, RDMA is not CXL. An RDMA-capable node is essentially still a request/response-based server. Maybe it is useful to mentally decouple operations into metadata and data, and use RDMA for the data path (common criticism is unnecessary RTTs for pointer chasing). Mercury[^5], with providers for libfabric etc, provides both messaging-style semantics for small messages and verbs-enabled RDMA via a _bulk_ interface for large messages.

Finally, I think the end-to-end argument does not preclude merging of layers for performance. I think it is a neat guiding principle for what to do in the absence of competing concerns, but it does not preemptively override the presence of competing concerns.

## What's Next?

I want to understand HPE Slingshot and UltraEthernet better, and maybe also start dabbling with CXL.

Side note: do you know PCIe uses CBFC? I think the gap between an interconnect, a fabric, and a network is smaller than we think, and loss-based mechanisms receive more academic attention than they should.

## References

[^1]: Datacenter RPCs can be General and Fast, _16th USENIX Symposium on Networked Systems Design and Implementation (NSDI 19)_, https://www.usenix.org/conference/nsdi19/presentation/kalia
[^2]: Homa: A receiver-driven low-latency transport protocol using network priorities, _SIGCOMM '18: ACM SIGCOMM 2018 Conference_, https://dl.acm.org/doi/10.1145/3230543.3230564
[^3]: Harmony: A Congestion-free Datacenter Architecture, _21st USENIX Symposium on Networked Systems Design and Implementation (NSDI 24)_, https://www.usenix.org/conference/nsdi24/presentation/agarwal-saksham
[^4]: Intel® Omni-Path Architecture Technology Overview, https://old.hoti.org/hoti23/slides/rimmer.pdf
[^5]: Mercury: Enabling remote procedure call for high-performance computing, _2013 IEEE International Conference on Cluster Computing (CLUSTER)_, http://ieeexplore.ieee.org/document/6702617/

_Updated on 20251008 to present a version that ages better._