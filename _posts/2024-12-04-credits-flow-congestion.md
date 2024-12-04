---
layout: post
title: Credits, Flow, and Congestion Control in Infiniband
date: 2024-12-04 14:00:36-0500
description: Notes on CBFC, lossless fabrics, receiver-driven congestion control etc.
tags:
  - networks
categories: systems
giscus_comments: true
related_posts: false
---
Things keep happening in datacenter networks. There (used to be) Ethernet, there's Infiniband, Omnipath[^2] (and its predecessors and successors), Slingshot[^3], UltraEthernet[^1], and now _Globally Scheduled Ethernet_[^4]. I don't get why they all need to exist concurrently and this is an initial attempt at unraveling this for myself.

Step 1 in this process is understanding Infiniband. Hyperscalers seem to like Infiniband and RDMA, but they also like their IP addresses and routing tables. RoCE and ROCEv2 were attempts to bridge the gaps, but they turned out to have problems. At this point, I know the talking points everyone rehashes --- PFC storms, HoL blocking, deadlocks... but I don't really understand any of it.

From my understanding, all of the changes in RoCEv2 were necessitated because it is hard to get RDMA to work over lossy networks. (As an aside, it seems to me that there is no such thing as a truly lossless network, but you can build a pretty good illusion of one with two properties: 1. Reduce the likelihood of packet loss, and 2. Handle retransmissions transparently at some lower layer). I haven't heard anyone complain about how flow control works in infiniband, so the key is maybe to understand it. This post is an attempt at that.

# Credit-based Flow Control in Infiniband
This is all based off slides here: [^5].
## Virtual Lanes and Service Levels
Credits are maintained per-VL on each HCA. VLs/SLs are technically different but equivalent for now. They are priority classes --- Infiniband supports up to 16. VL15 is reserved for subnet management traffic, while the others are available for regular data. The difference is that the application requests service levels, and the SL-VL mapping is a management decision handled presumably by the subnet manager.
## Basic Numbers
- Each `Flow Control Block` is 64B.  One 64B send requires one credit to be authorized.
- A VL will issue a maximum of 2048 credits, which translates to a 128KB receive buffer.
## CBFC Actual
There are 3 main terms: `ABR`, `FCCL`, `FCTBS`.
- `FCCL`: the credit limit (the max point up to which the sender has been authorized to send).
- `ABR`: total blocks received at the receiver so far.
- `FCTBS`: total blocks sent.

`FCTBS` - `ABR`: blocks in transit on the wire.
`FCCL` - `FCTBS`: remaining credits for the sender. A send will be permitted if the size is smaller than this limit.
# Flow Control vs Congestion Control
Flow control makes infiniband largely and inherently lossless. Rare occasions that cause packet corruption etc. may require retransmissions. The fabric will do retransmissions for you if `Reliable Connected` was requested. CBFC kicks in regardless of whether you use RC or UC or UD. I haven't looked into how retransmissions for `RC` are managed.

Infiniband also has congestion control on top of flow control. Why both need to exist is not entirely clear to me yet. What I do know is that IB employs some variant of `ECN (Explicit Congestion Notification)` to help detect congestion (`FECN` and `BECN`). I don't know what the endpoints do in response to ECNs.
# Questions For Myself
- Why is it hard to retrofit CBFC on to ethernet?
- Why don't all datacenter fabrics use CBFC?
- How does CBFC compare to loss-based congestion control.
# References

[^1]: UltraEthernet: Overview of and Motivation for the Forthcoming Ultra Ethernet Consortium Specification, , , 
[^2]: What If Omni-Path Morphs Into The Best Ultra Ethernet?, , 2024, https://www.nextplatform.com/2024/06/26/what-if-omni-path-morphs-into-the-best-ultra-ethernet/
[^3]: Cray's Slingshot Interconnect Is At The Heart Of HPE's HPC And AI Ambitions, , 2022, https://www.nextplatform.com/2022/01/31/crays-slingshot-interconnect-is-at-the-heart-of-hpes-hpc-and-ai-ambitions/
[^4]: Whitepaper on Globally Scheduled Ethernet, , 2024, https://regmedia.co.uk/2024/11/26/china_mobile_gse_whitepaper.pdf
[^5]: Infiniband Credit-Based Link-Layer Flow-Control, , 2014, https://www.ieee802.org/1/files/public/docs2014/new-dcb-crupnicoff-ibcreditstutorial-0314.pdf