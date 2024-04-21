---
layout: On reasoning, autonomy, intelligence etc.
title: On reasoning, autonomy, intelligence etc.
date: 2024-04-21 17:31:58-0400
description: Or what would it take to get to agents with these properties.
tags:
  - "#ml"
  - "#llm"
  - "#reasoning"
categories: ml
giscus_comments: true
related_posts: false
---
So the topic for this post is a bit out of my wheelhouse. The primary purpose of this post is to flush some thoughts that are brewing in my head so that I can get back to my day job. Everything else is secondary. I should warn anyone reading this that I have no particular background in these topics, nor have I done a decent job of keeping up to date on related work. This post will have no references - it may be completely off-track, or reasonable but outdated, or exist in any other defined epistemic state. _Caveat Emptor._

Over this post, I will explore five topics - intelligence, autonomy, reasoning, planning, and consciousness. This has been obviously prompted by the hottest thing to happen this decade (LLMs). Let me structure this post as a series of theses and rationales.
## LLMs, As Currently Designed, Can Not Be Reasoning

This idea emerged in my head in the early days of GPT-3. Its prowess was shocking, and everyone started reassessing everything (_autogaslighting_).

This intuition is simple --- LLMs generate text at a constant token rate, and an intelligent agent simply can not do that. For a simple query, an intelligent agent is able to respond instantly, while for a complex query, it needs to go and _think_ and _plan_ a response. There can not be any upper bound to the amount of time this takes.

LLMs seem to encode some constant amount of capability. It is perfectly okay for a new (yet not fully optimized architecture that is on the right track) to take more time than necessary for a simple query, but an architecture that can not take an infinite time can not be reasoning.

More specifically, an inference agent that is thinking and planning will have some `while`-loop like structure in some shape or form.
## Intelligence Is Poorly Defined

I am sure there is material by scientist-philosophers exploring the definition of intelligence. I have not read any of it. The thesis is that it is am ambiguous phrase encapsulating all the flaws of natural language, and is best avoided. The other four words, in my head, lend to much cleaner definitions.

1. **Reasoning** - The ability to model a situation as statements in some form of logic (say propositional logic), and prove them to be correct as per the rules of that logic.
2. **Autonomy** - The ability to operate independently in pursuit of some objective.
3. **Planning** - The ability to decompose a complex problem into a series of subproblems. This is very much like A* search --- it is recursive, and may require backtracking. It is essentially a solver, and benefits from some "intuition", which is a set of heuristics that produce a partial solution quickly and speed up the solver. It also requires an ability (intrinsic or external) to know if the objective has been met.
4. **Consciousness** - It is simply a state of heightened autonomy, where an agent is able to choose its objective function, and change it at any point.
## Consciousness Emerges from Autonomy and Reasoning

In the previous subsection, I was trying to go for definitions that allow the respective traits to exist independently, albeit complementarily. I do not think I fully succeeded.

An ant, I think, has autonomy and planning. I find it hard to separate the two --- an autonomous object that can not plan would just not survive (survival! life! an objective function! natural selection!). 

It was very hard to define planning as something independent of reasoning. I think that that's possible, though. An ant does not need to be able to reason that it has eaten and that it can temporarily stop hunting for food. It either reaches that state or "nature" lets it die. Over time, only ants that can recognize that state survive. Even then, they can only recognize specific states, and can not reason in general terms. _Reasoning is not necessary for autonomy._

I think it also holds in the other direction. _Autonomy is not necessary for reasoning_. A solver that matches a set of statements to a type of logic does not have to be autonomous.

Planning, I think, is not strictly necessary for reasoning, but it is key to making it an interesting trait. A solver that can only evaluate given statements for compatibility with the axioms of a logic would be a boring solver. A solver that can translate a _situation_ into valid logical statements, and reconcile them with some past state of the world in its head is far more interesting. Does this imply/require autonomy? I think it does not.

Finally, the combination of autonomy and reasoning is powerful. Such an agent is autonomously able to recognize the achievement of a certain objective (without an incentive from nature). This leads to an ability to choose between objectives, which, I argue, is a sufficient condition for the emergence of what I call consciousness.

Computationally, an autonomous reasoning conscious agent has a randomly accessible set of objectives. It context switches to some objective based on some meta-heuristic, and runs an A* search on that objective. If it fails, it knows that it has failed, and keeps backtracking. If it succeeds, that objective is marked completed. A _smarter_ agent is either quick in succeeding, or succeeds more often than others. But both smart and less-smart agents have the same fundamental architecture, and an ability to recognize that an objective is not met.
## An AI Agent Does Not Necessarily Need To Be Conscious

If reasoning and planning can be accomplished without autonomy, that is sufficient to get to a really powerful level of assisting agents. If such agents are not autonomous, they are not conscious, and this allows us to circumvent a whole host of ethical concerns. 

This would be somewhat akin to taking a snapshot of a 25-year old's head, and using that snapshot to run queries. Since the snapshot is not autonomous, it does not accumulate more knowledge, but is able to serve an infinite amount of queries being a "non-alive" "non-conscious" program.
## Incorporating Logic Into Training

How do you train your models in a way that produces reasoning and planning?

One way may be that the training process is seeded with a preferred logic and its axioms. Each training iteration does something akin to producing an A* plan on a given goal, validating the plan with respect to the logic, and using the loss to make changes to various components if the logic is violated. 

The components could be:

1. The A* "intuition"
2. The natural language translation "intuition" (translate natural language into logical statements and vice-versa)
3. A world model (as a series of statements/metastatements in the logical format)

Each "intuition" IMO, is a proxy for a neural net. The entire apparatus is a series of neural nets and an architecture that are co-trained, until they start converging to some reasonably low loss.
## Can Logic Emerge Naturally?

Is it possible that some deep learning architecture automatically learns something that resembles this structure? After all, we humans developed different logics from scratch. Maybe there are other sets of axioms that are "better" and these models automatically stumble upon them?

I think hacking this loop manually is necessary, because we want agents that can reason and plan, but not be autonomous. Autonomy requires us to think about all sorts of complicated things --- are these things alive, should they have rights, do they like us, are they aligned the way we want them to? Best to circumvent these if possible.
