---
layout: post
title: Are All Networks Just Tradeoffs?
date: 2024-12-06 19:58:30-0500
description: Or, are we destined to tune?
tags:
  - tag
categories: cat
giscus_comments: true
related_posts: false
---
[Part 1 here](https://ankushja.in/blog/2024/credits-flow-congestion/).

This post will explore the following thesis:
1. All networks and variants are tradeoffs.
2. If there are tradeoffs, there is no permanent winning. You are always tuning to chase _the window_.

Disclaimer: this could be the most obvious statement in the world. Or maybe deep within the symbolic mines of queuing and scheduling, someone has said something that disproves all of it. Or maybe that that statement is obvious but the arguments below are flawed. I have no idea --- this blog does not come with any guarantees for rigor or scrutiny.
## Context: Thinking About CBFC vs PFC
The thing in the back of my mind recently has been --- why does everyone complain about PFC and RoCEv2, and why do they not complain about Infiniband and CBFC (Credit-based Flow Control). Why could RoCEv2 not adopt CBFC? What do you gain and what do you lose? Do you still need higher-level congestion control with CBFC?
## CBFC Is Not A Magic Pill
An upper bound to CBFC goodness is much easier to establish than its precise extent.

CBFC is not a magic pill. It can still lead to credit loops, head-of-line blocking, buffer overflows, packet loss emanating from it, and so on. It is also amenable to tuning: routing, topologies, credit management schemes etc. to reduce the likelihood of bad things happening.

CBFC absolutely provides no theoretical guarantee (I'm not talking about a bounds-type argument: under X flows and Y buffer sizes you prove a Z\% upper bound on packet loss). Also not everyone means the same thing when they talk about CBFC --- the Infiniband spec on this is not very prescriptive --- my understanding is that it describes packet formats, and some basic mechanics, but still leaves a lot of room for vendors to do better.
## Guarantees Are Expensive
You could provide a lot of guarantees by implementing a network as an all-to-all network of separate links. That is essentially what a crossbar is. But we want to optimize for cost. So we do tiers and routing and non-uniform bandwidth and all that stuff. You lose out on worst-case performance but that's the only way to get systems to scale.

Turns out that this applies for everything --- including tail latencies, jitter etc. The only way to guarantee that you will move a packet in a predictable timely manner is to explicitly carve out room for that packet on the path before sending it out. If you care about maintaining a high utilization or cost or scalability, this is bad.

Given a guarantee, you can always make an argument that "we can relax this guarantee a little and get a lot more performance in the common case." This is statistical multiplexing or oversubscription or optimistic concurrency control or whatever. These are incredibly important --- these thoughtful relaxations are the reason that systems work and can be built for the prices that're built for. But it is always nice to be explicit about what you are losing in return.
## Overloading Creates More Risks
As the goal of this exercise was to understand CBFC, let us compare it with sender-driven mechanisms. Sender-driven congestion control overloads certain signals to infer network state --- RTT and packet loss seem to be two of them. This works until something happens that changes the meaning of these numbers --- bufferbloat being one example. An advantage, in principle, of CBFC is that it is explicitly communicating actual network state, so theoretically, it should be robust to some such issues. I do not know if that is actually realized in practice.

This is in no way trashing sender-driven mechanisms. A good system is one that gets the job done --- clean conscience and mathematical elegance are the domains of whiteboard hoggers. The end-to-end principle and this layered approach to TCP/IP has taken us a long long long way. Overloading those signals is the practical thing to do. (Also note that I'm conflating flow control with congestion control --- CBFC is very much the former, but I guess it dictates and comes bundled with a different congestion control in IB with ECNs and injection throttling).
## Expectations for Future Congestion Control
This post is a precursor to me trying to understand all the cool new things in datacenter fabrics --- Omnipath, Slingshot, UltraEthernet, maybe Globally Scheduled Ethernet?

If these arguments hold, none of these systems' mechanisms will be perfect. There will always be cases where Bad Things$^{TM}$ happen. Part of the argument is that that may be okay, and an evaluation of their properties must be holistic.
## Some Degree Of Tuning Is Okay?
- I can not pick an outfit that works in all weathers. I am destined to keep tuning.
- Some tuning is worse than others. If I wore an outfit that had only one shoe, I would have to hop and keep swapping my shoe from one foot to the other. 
- An outfit that covers the expected swings over one day is sufficient for an outfit.
- A bag that covers the expected swings over one week is sufficient for a short trip.
- A wardrobe that covers the expected swings over the year in Pittsburgh is sufficient for most other cases.

What are the takeaways for systems?
- We are destined to tune. We should plan for that.
- It would be nice if we understood systems in terms of their coverage of design space.
- Nothing in this discussion rules out the existence of systems that cover strictly more of the design space than others. Probably someone has and/or will prove that certain aspects are pareto-optimal. But it's still a small sheet over massive legs.
## Chasing The Global Optima
Network sharing and scheduling mechanisms are probably by far the most well-studied and deployed examples of a distributed system trying to construct/reach a global optimum, and both mathematical and practical arguments of the challenges that comes with.

All systems would benefit from better decisions. Better decisions are enabled by a better view of the system state. But constructing this system state may be prohibitively expensive. It may also be a moving target. It will definitely have some uncertainty bounds because physics. It may also be possible that explicitly constructing the system state is not necessary --- we can apparently go quite a bit with individual actors acting on simple rules. (Something about game theory and cooperative games comes to mind but I'm already wayyyy past my depth here).