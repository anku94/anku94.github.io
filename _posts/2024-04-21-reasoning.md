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
published: "false"
---
So the topic for this post is a bit out of my wheelhouse. The primary purpose of this post is to flush some thoughts that are brewing in my head so that I can get back to my day job. I should reiterate that I have no particular background in these topics, nor have I done a decent job of keeping up to date on related work. This post will have no references --- it may be completely off-track, or reasonable but outdated, or exist in any other possible epistemic state. _Caveat Emptor._

Over this post, I will explore five topics --- intelligence, autonomy, reasoning, planning, and consciousness. This has been obviously prompted by the hottest thing to happen this decade (LLMs). Let me structure this post as a series of theses and rationales.
## LLMs, As Currently Designed, Can Not Be Reasoning

This idea emerged in my head in the early days of GPT-3. Its prowess was shocking, and everyone started reassessing everything (_autogaslighting_).

This intuition is simple --- LLMs generate text at a constant token rate, and an intelligent agent simply can not do that. For a simple query, an intelligent agent is able to respond instantly, while for a complex query, it needs to go and _think_ and _plan_ a response. There can not be any upper bound to the amount of time this takes.

LLMs seem to encode some constant amount of capability. It is perfectly okay for a new (yet not fully optimized architecture that is on the right track) to take more time than necessary for a simple query, but an architecture that can not take an infinite time can not be reasoning.

More specifically, an inference agent that is thinking and planning will have some `while`-loop like structure in some shape or form.
## Intelligence Is Poorly Defined

I am sure there is material by scientist-philosophers exploring the definition of intelligence. I have not read any of it. The thesis is that it is am ambiguous phrase encapsulating all the flaws of natural language, and is best avoided. The other four words, in my head, lend to much cleaner definitions.

1. **Reasoning**. The ability to model a situation as statements in some form of logic (say propositional logic), and prove them to be correct as per the rules of that logic.
2. **Autonomy**. The ability to operate independently in pursuit of some objective.
3. **Planning**. The ability to decompose a complex problem into a series of subproblems. This is very much like A* search --- it is recursive, and may require backtracking. It is essentially a solver, and benefits from some "intuition", which is a set of heuristics that produce a partial solution quickly and speed up the solver. It also requires an ability (intrinsic or external) to know if the objective has been met.
4. **Consciousness**. It is simply a state of heightened autonomy, where an agent is able to choose its objective function, and change it at any point.
## Consciousness Emerges from Autonomy and Reasoning

In the previous subsection, I was trying to identify orthogonal pieces of the whole "intelligence" puzzle, by defining the traits in a way that allows them to exist independently, albeit complementarily. I do not think I fully succeeded. Let us take arbitrary pairs from the above set and evaluate their pairwise indendence.
### Autonomy and Planning

An ant, I think, has autonomy and planning. I find it hard to separate the two --- an autonomous object that can not plan would just not survive (survival! life! an objective function! natural selection!). 
### Autonomy/Planning and Reasoning

Can planning exist independent of reasoning? Without prejudice or malice towards other species, let us consider ants. We choose ants because while they definitely plan, we may be able to dwell on whether they reason to unfold insights. Let us model ants as single-objective species --- they need to be able to seek food, plan in a way that leads to food, and recognize that they have eaten adequate food. They do not think about food symbolically, but are able to pattern-match certain states via feedback loops (feeling hungry, full, there is probably food in that direction etc.). I feel like this is an a-ha moment --- planning does not require symbolic reasoning, but it does require some ability for feedback and pattern matching. I think modern autonomous vehicles might exist in this territory.

I think the other direction is much clearer. _Autonomy/planning are not necessary for reasoning_. A solver that matches a set of statements to a type of logic does not have to be autonomous.

While planning, I think, is not strictly necessary for reasoning, it is key to making it an interesting trait. A solver that can only evaluate given statements for compatibility with the axioms of a logic would be a boring solver. A solver that can translate a _situation_ into valid logical statements, and reconcile them with some past state of the world in its head is far more interesting. Does this imply/require autonomy? I think it does not.
## Where Does Consciousness Fit In?

Say you endow an agent with autonomy and symbolic reasoning. Presumably, it also has the capability to observe and interact with the world. If such an agent was not programmed with a meta-objective, except maybe an instinct to survive and reproduce, it would eventually create replicas, develop a sense of self and universe, contemplate about its place in the universe, and over time and iterations acquire consciousness. This requires some ability for self-mutation, but that ability is implicit --- if an agent is not able to mutate itself, it can apply the mutation to a descendent. I think the distinction between the two is arbitrary, as in the distinction between modify-in-place and copy-on-write. (Although the former would speed up "convergence" by orders of magnitude.)
## An AI "Entity" Does Not Necessarily Need To Be Conscious

If reasoning and planning can be accomplished without autonomy, that is sufficient to get to a really powerful level of assisting entities. If such entities are not autonomous, they are not conscious, and this allows us to circumvent a whole host of ethical concerns. 

This would be somewhat akin to taking a snapshot of a 25-year old's head, and using that snapshot to run queries. Since the snapshot is not autonomous, it does not accumulate more knowledge, but is able to serve an infinite amount of queries being a "non-alive" "non-conscious" program.

The reason I use the word "entity" here is because "agent" implies "autonomy" in my head. I think we can have two kinds of entities --- a "planner/reasoner", and an "agent".
## Computational Models
### Of A Planner

Computationally, a planner has:

1. A data structure that is essentially a knowledge graph. It is traversable and approximately indexable. I think the whole embedding and vector search area is approximately there in terms of looking up this structure. But we do not have a way of representing this structure as a series of clear, unambiguous axioms.
2. A small LLM, which is essentially an interface to natural language (I think we currently have large LLMs because we are trying to get reasoning to emerge inside them, but all we really need is a natural language interface, and something around 10B parameters is good enough for that.)
	1. The LLM converts a natural language query into a series of symbolic reasoning tasks
	2. It defines an objective function

### Of An Agent

Computationally, an autonomous reasoning agent has a randomly accessible set of objectives. It context switches to some objective based on some meta-heuristic, and runs an A* search on that objective. If it fails, it knows that it has failed, and keeps backtracking. If it succeeds, that objective is marked completed. A _smarter_ agent is either quick in succeeding, or succeeds more often than others. But both smart and less-smart agents have the same fundamental architecture, and an ability to recognize that an objective is not met.

## An AI Agent Does Not Necessarily Need To Be Conscious

If reasoning and planning can be accomplished without autonomy, that is sufficient to get to a really powerful level of assisting agents. If such agents are not autonomous, they are not conscious, and this allows us to circumvent a whole host of ethical concerns. 

This would be somewhat akin to taking a snapshot of a 25-year old's head, and using that snapshot to run queries. Since the snapshot is not autonomous, it does not accumulate more knowledge, but is able to serve an infinite amount of queries being a "non-alive" "non-conscious" program.
### On Alignment, Life, and Other Ethical Debates

This line of reasoning has verged too close to certain hot topics.
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

# LLMs are Language + Intuition

What are intuition/instinct? Instinct can partially/maybe be understood as intuition but for motor movements? Intuition is far more interesting.

Can we model intuition as a "semantic cache"? It responds instantly. It can get us pretty close to the real answer if it is well-calibrated. It can be off if it is uncalibrated.

How do we validate intuition? We have to defer to data and symbolic reasoning --- we either do it ourselves from first principles or refer to existing works.

Intuition is super important --- it would be exhausting and unproductive to derive everything from first principles. Intuition is maybe how we bootstrap intelligence and symbolic reasoning is how we make it robust.

So can we model LLMs (and maybe other language model architectures) as intuition? I think we can, and that leads to some pretty interesting conclusions:

1. Scaling transformers to trillions of parameters etc. is the equivalent of trying to build an intuition so powerful that it obviates the need for symbolic reasoning. A powerful all-knowing intuition can be extremely useful, as is being demonstrated, but it is not a substitute for reasoning.
2. One way it falls short off human-type reasoning is that current architectures can not recalibrate their intuition by continuous learning.
3. We (as a civilization) have cracked the basic mechanic of intuition. Of course, different models will continue to emerge with varying capabilities, and that is the equivalent of having different cognitive abilities.
4. Computers can already do symbolic reasoning. And LLMs are also "there" in terms of their ability to interface with natural language. So we have the "primitives" for "AGI"?
5. We are already augmenting LLMs with symbolic capabilities. This is what happens when ChatGPT writes python code to do some math for a user query, vs generating the math directly.

IMO, the ultimate reasoning architecture would:

1. Have an "intuition" that supports online learning (as in, actually change model weights, not just hack in RAG or whatever)
2. Have a "knowledge base" data structure
	1. This supports "approximate semantic search" (embeddings + K-approxiate nearest neighbors is pretty much there I think)
	2. Can be populated externally, and modified dynamically
3. Have an orchestrator process that is essentially an A* searcher. 

The orchestrator is hard, because the "plan" can be a mix of "solver tasks" + "actions". The actions could be from a list of actions available to the agent, such as looking up the web, emailing someone, trying something else... how long to try? When to give up? When to ask the user for more input?