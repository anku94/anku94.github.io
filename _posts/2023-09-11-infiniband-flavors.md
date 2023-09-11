---
layout: post
title: The Varied Flavors of Infiniband
date: 2023-09-11 15:05:42-0400
description: Some description
tags: networks
categories: systems
giscus_comments: true
related_posts: false
---

This is an attempt to track and understand all the different "flavors" of Infiniband-like interfaces that are around, active, or relevant.

Thinking of things like PSM, PSM2, OFI, Verbs, UCX etc. I doubt this particular post will have anything insightful --- this is more of a placeholder for more insightful things in the future.

## Pre-historic Times (1995-2002)

Most HPC clusters had proprietary networks, with their own [MPI providers][1]. Some weird-sounding names: MPICH-MX, MPICH-Elanlab.

## Ancient Times (1995-2002)

InfiniBand: long awaited HPC network standard. Comes with OFED open-source networks stack, the `verbs` API. MPI implementations started using Verbs.

## Pre-Modern (2005-2010) and Modern (2010-Now) Times

### Performance-Scaled Messaging

Needs supposedly start outstripping the capabilities of the standards. PSM (Performance-Scaled Messaging) is introduced.

#### PSM Owner History

There used to be this company called QLogic. They developed network hardware, including "Infiniband", in the pre-modern times.

Their IB was compatible with the Verbs API, but was developed truly for this interface called PSM. They acquired PathScale (a compiler vendor, among other things maybe?) in 2006, and developed _InfiniPath_, also marketed as _TrueScale_ --- a network interface that was Infiniband-compatible but supported PSM for better performance.

They were later sold to Intel. Their tech became the basis of a second-gen interconnect called _Omni-Path_. Omni-Path used an evolution of psm called psm2, which was not backward-compatible. The psm/Qlogic stuff was 40 Gbps, psm2/Omni-Path was 100 Gbps. As per [this][3], Omni-Path also incorporated features from Gemini and Aries interconnects bought from Cray in 2012.

Something happened at Intel around 2019 --- they canceled the 200 Gbps variant of Omni-Path. In 2020, a company called Cornelis Networks was spun out to carry Omni-Path forward.

[Cornelis][2] still exists, and are continuing the development of Omni-Path-based products.


#### PSM Technical Details

This is more of questions and references.

> “The software infrastructure of InfiniBand, based on verbs, is really based on the original goals of InfiniBand, which was to replace PCI-X and Fibre Channel and maybe Ethernet,” Murphy tells The Next Platform. “Verbs were not structured at all for high performance computing. PathScale created Performance Scale Messaging, or PSM, which was totally independent of InfiniBand verbs and was a parallel transport layer specific focused on HPC. In the enterprise, when I am talking to 40 or 50 disk drives or 40 or 50 queue pairs, I can put that on my adapter’s cache and it works great. But in HPC, when I have a node with a hundred cores and a thousand nodes, this becomes a giant scalability problem we just cannot manage in the adapter’s cache. PSM could do this better, but even this was invented two decades ago and the world has continued to evolve.

It seems one of the considerations for PSM was the NIC SRAM overhead of creating Verbs Queue Pairs. NIC SRAM is finite, and for all-to-all type communication patterns, the SRAM can not fit all the contexts. This [paper](https://www.usenix.org/system/files/conference/osdi16/osdi16-kalia.pdf) also talks about prefering RDMA UDs over RCs. With RDMA UD, one queue pair can be used for multiple destinations, and the total number of QPs can be controlled. We don't want CPU cores contending over UDs, so one QP/core is still desirable, but it scales with the number of cores, instead of the number of destinations, which is a lot more tractable for large clusters.

One of the references also talks about dynamic congestion detectioni and rerouting borrowed from Aries and incorporated into Omni-Path.


- What are other design advantages of PSM over Verbs?

### Mellanox and Nvidia

Something about Mellanox hacking Verbs, with "Accelerated Verbs", MXM, UCX, RoCE, GPUDirect ...

### HPE and Slingshot and UltraEthernet

Similar stuff?

### Then there is CXL

Phew.

[1]: https://agullo-teach.gitlabpages.inria.fr/school/school2019/slides/mpi.pdf
[2]: https://www.nextplatform.com/2021/07/09/a-third-dialect-of-infiniband-in-the-works-again/
[3]: https://www.nextplatform.com/2023/08/24/cornelis-unveils-ambitious-omni-path-interconnect-roadmap/
