---
layout: post
title: Special Cases Can Not Produce Generality
date: 2026-06-24 23:32:53
description: Or an argument for human-maxxing
tags:
  - systems
categories: philosoraptormode
giscus_comments: true
related_posts: false
ignore: false
---

This post explores the origin and limits of prediction. The motivation here is again LLMs---predictive machinery taking the world by storm and inducing hysteria about the future of everything. This post will attempt plant a pro-humanity flag in the landscape of positions without getting on highway dogma.

Let us first explore the origin of prediction, and on that quest, let us first try definitions of the term and see what fits. 
- Is it... using the rules of the environment to tell what happens tomorrow? A ball dropped from a 10m building will hit the ground in 1s (numerical accuracy of the basic physics employed here is not necessary for this exercise). Is this just science?
- But what if the rules are intractable? There exist methods for predicting weather, but let us say I do not have access to this weather prediction infra. I can make conditional predictions: if there are clouds, it will rain.
- Will it definitely rain if there are clouds? Here we branch into science and bayesian reasoning. Science allows definite claims with errors... or does it? Weather prediction is also probabilistic, with ensemble models and what not. So is science just "principled application of hand-wave" and bayesian reasoning "vibes-based hand-wave"?
- What is bayesian reasoning? This one is easy: it is just the application of formal principles to a set of probabilistic inputs. It does not concern itself with how they were derived but just allows principled synthesis, and as such is not really a primitive.
- Is the environment always deterministic, i.e. does it always lend itself to a predictive model? One source of uncertainty is rapidly evolving fine-grained phenomena that we refuse to model. Air molecules have frenetic and unique trajectories, but for most purposes it suffices to model air as having a temperature: statistical physics where we can model an ensemble without needing to model individual entities, insofar as the behavior is amenable to this approach. Another source of uncertainty is agentic behavior: what will the drivers and pedestrians do on the road tomorrow?
- Is inferring the rules of the environment necessary for prediction? ML models predict all the time without learning natural laws, while humans supposedly do learn natural laws. The natural law process seems to be highly robust and while its origin is hard to point out, millions of years of evolution enable a circular description: principles that reliably confer survival.

Ultimately, the goal of prediction is the agent's survival. Famines mean you ration food. Rain means you pack an umbrella. Reasoning is an approach to prediction that does not accumulate error, and hence be compounded and composed indefinitely. Note that this does not salvage reasoning, because the process of modeling reality into reasoning frameworks is intrinsically error prone, and it is trivial to arrive at formulations of problems that are not amenable to zero-error solutions. We therefore try relaxations where we deliberately and consciously accept errors for approximate solutions.

But regardless of whether it is math or ML models, prediction has a finite horizon and humans _deal with it_ all the time. The model said it would rain but did not. Claude said it fixed the bug but it did not. The key to human survival is not the NWS or Sam Altman, but the ability to respond to the residual between reality and prediction. Note that unless we can perfectly simulate the universe, a non-zero residual exists by definition, and the only tool that tames that monster is _adaptation_.

In fact---and we finally arrive at the core thesis of this post---adaptation is the necessary and sufficient condition for agents' existence, and prediction is just a special case of approaches for reducing adaptation latency. If you can anticipate, you can formulate strategies that you could not have otherwise. But it is the capability that picks up the tab when prediction falls short, which it does by definition.

So what is the point? LLMs are predictive engines. They are a statistical compression of our knowledge, like a generative textbook. Just like it is a category error to say my math textbook is smarter than me or can do my job, the same applies for LLMs. This is not to say that there can not exist a pytorch-executable DNN that can adapt. The argument is simply that we have no evidence of that capability emerging as a result of all the scaling over the last few years.

**Why this might be good, actually.** An example of adaptive systems is the bubonic plague. Another example is the COVID-19 virus. These and multiple examples in their class demonstrate that the upper bound for an adaptive system is devastating. These systems are always fuzzing against their environment to replicate. Note that intent is a poor rubric to reason about agents: the COVID-19 virus did not wake up and decide to be mean to me. That predictive systems can not grow adaptive bones is good. It makes it impossible for a Waymo to one day emerge the ability to decide that it does not my incendiary statements against machines and run over me.

**What does this mean for jobs?** A piece of technology does not need to be AGI to profoundly affect jobs. Cars affected jobs, and so did washing machines, batteries, computers, smart phones etc. There is a transition period where accountants argue that the tech will eliminate their jobs, a new equilibrium of higher productivity is reached, peace holds for a few years until the next such thing. This one is no different.

For a _positive conclusion_ (positive as in predictive, not ruling-out), let us apply Amdahl's Law to jobs: currently they are \(x\%\) prediction and \(y\%\) adaptation. Take coding: sometimes I need to [stare at core dumps](https://ankushja.in/blog/2024/inscrutable-core-dump/), other times I am writing `printf` statements to assist with debugging. The parting thought is this: what happens if we apply infinite speedup to the \(x\%\)?

**EDIT**: Actually, I lied. Modern LLMs are somewhat recursive: they predict, there is a residual, they then learn to predict the residual, and so on, and the amount of time they can work before the leash needs to be yanked goes up. The residual framing tells us that there must be an upper bound. But in the short run, the benchmark is not AGI. The benchmark is: _can we find other avenues to divert human adaptivity to faster than LLMs gobble up the predictive components of their current avenue?_ The answer to this could very well no, and while you could argue for this to just be a system that has not achieved its steady state, systems' unsteadiness can last longer than human careers.