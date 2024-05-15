---
layout: post
title: "On Intelligence: Assessment and Direction"
date: 2024-05-15 01:53:05-0400
description: How far have LLMs gotten us? What remains? What will "the rest" take?
tags:
  - ml
  - llm
  - aligners
categories: ml
giscus_comments: true
related_posts: false
---
So the topic for this post is a bit of a departure from my usual mucking in the sewers that modern systems are. I have been fascinated by LLMs, and what they are missing enroute to "AGI". This is a collection of some of those thoughts that have been brewing over the past few months. I am not particularly familiar with the related work in this area, and this is mostly coming from first principles, with some random inputs from here and there folded in.

I have no calibration for how much of this is just me reiterating what is already known and well-understood, or obvious, or deeply flawed.
## LLMs, As Currently Designed, Can Not Be Reasoning

This idea emerged in my head in the early days of GPT-3. Its prowess was shocking, and everyone started reassessing everything (_autogaslighting_). And then we started noticing a million ways to "crack" it, relaxed a little, and things got better with GPT-4/4o.

This intuition is simple --- LLMs generate text at a constant token rate, and an intelligent agent simply can not do that. For a simple query, an intelligent agent is able to respond instantly, while for a complex query, it needs to go and _think_ and _plan_ a response. There can not be any upper bound to the amount of time this takes.

LLMs seem to encode some constant amount of capability. It is perfectly okay for a new (yet not fully optimized architecture that is on the right track) to take more time than necessary for a simple query, but an architecture that can not take an infinite time can not be reasoning.

I have come across the term "out-of-distribution" to describe hallucination etc, and I think it offers a good way to think about LLMs --- they form a distribution over all that is known, and are able to generate samples from that distribution. For why this does not amount to reasoning, read on and I think you will have a better idea of how this is going.
## LLMs as a Snapshot of Intuition

I think LLMs are a lot more similar to _intuition_. Intuition is the mechanism by which we generate instant responses --- these can be right, or wrong. I say _a snapshot of intuition_ because human intuition constantly refines itself, and model weights are static.

Intuition is a different property from _planning_ and _reasoning_. I will describe this more in the "human learning" section --- I feel that there are circular dependencies here and I can not seem to figure out a great order to put this in.

Drawing an equivalence between LLMs and intuition has two interesting corollaries:
1. It provides an explanation for why we are building massive and expensive models. This is somewhat similar to building an intuition so strong that you make up for reasoning.
2. It maps them to a component of the grand architecture of "human cognitive ability". This would imply that while we (as the human race) have not yet figured out the entire architecture, this is fundamentally similar to a building block.

I do feel that the fundamental approach to synthesizing "capability" by "exposing" a neural network to lots of data is valid. This is in contrast to coding and program synthesis, where capability is hand-crafted line-by-line. This is not to say that the latter approaches are not valid, but that the former allows for capabilities the latter does not (and vice-versa).
### A Model of Human Intelligence

I think my point should make a lot more sense if I explain my model of human intelligence.

Say a "rational" human being is asked a question (say a physics situation involving some bodies). This is the sequence of steps they take:

1. They have an initial intuition of how they expect the system to behave.
2. They try to formally solve it by modeling it as a set of equations, solve the equations, and get a result.
3. Let us pretend that they get a result that they believe is "counterintuitive". They recheck their math and if it holds, accept that "while my intuition suggests otherwise, this must be true."
4. Over time, their intuition internalizes what the math says, and a year later if they are asked a similar question, their instinct is a lot closer.

Now we can define _reasoning_ and _planning_. 

- *Reasoning* is just modeling a situation as a set of logical statements, and them symbolically validating those statements.
- *Planning* is decomposing a problem into a series of subproblems, possibly recursively, and solving the smaller subproblems, and composing all the leaf nodes into a solution for the bigger problem.
	- The "plan" for an "agent" can include "actions". Over the course of trying to solve a problem, they may ask other agents for assistance, build machines, or take any other action within its scope.

"Agents" also "meta-reason" and "meta-intuit". They think about whether their plan is logically valid or not. They have different preference profiles over the set of candidate actions. (Some are more likely to approach other agents, others may prefer choosing goals that avoid interactions etc.) These heuristics lead to emergent traits such as personality, extroversion, neuroticism etc.
## A Lesson from Flight

Now how does all this apply to how to build such capabilities? That is the quadrillion dollar question.

How humans cracked flight is, in my opinion, an instructive parallel. That birds could fly established that flight is possible. However, the mechanics we use to actually fly are very different --- our aircraft do not flap their wings. We probably still can not build a meaningful wing-flapping aircraft. That in no way limits our ability to leverage aviation and structure our entire economies around that capability being commonplace.

The same holds for LLMs. They need _reasoning_ and _planning_, but the way they achieve these capabilities may be very different from the way we evolved. Life evolved as a self-sustaining Minimal Viable Product that could mutate to gain capabilities. We may be able to stitch together a "self-sustaining cognitive loop" directly from larger pieces. Or we may find that the easier way to do it is to build simpler agents and let them self-mutate to acquire capability.

I think a variety of architectures are possible --- autonomous and not. It is not necessary that they are conscious, "alive", have free will, have feelings, etc.
## A Lesson from Organic Chemistry

Before the 18th century, we believed that certain molecules, associated with living beings, had an inherent life force, and therefore could not be synthesized artificially. From Wikipedia:

> In 1828 [Friedrich Wöhler](https://en.wikipedia.org/wiki/Friedrich_W%C3%B6hler "Friedrich Wöhler") produced the _organic_ chemical [urea](https://en.wikipedia.org/wiki/Urea "Urea") (carbamide), a constituent of [urine](https://en.wikipedia.org/wiki/Urine "Urine"), from _inorganic_ starting materials (the salts [potassium cyanate](https://en.wikipedia.org/wiki/Potassium_cyanate "Potassium cyanate") and [ammonium sulfate](https://en.wikipedia.org/wiki/Ammonium_sulfate "Ammonium sulfate")), in what is now called the [Wöhler synthesis](https://en.wikipedia.org/wiki/W%C3%B6hler_synthesis "Wöhler synthesis").

It was then that we realized that organic molecules have nothing inherently different from others. They could be synthesized, hacked, and novel ones could be created to trick our bodies into working a certain way.

I think that to the extent we think about intelligence as something inherent to humans, we will shortly be proven wrong. I also think that it will be less of a breakthrough moment than a series of continual improvements of the kind we are currently in the midst of --- deeply shaping the way we work and organize human productivity along the way.