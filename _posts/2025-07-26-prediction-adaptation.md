---
layout: post
title: Prediction and Adaptation in Decisions
date: 2025-07-26 16:59:58
description: How to model decision-making itself?
tags:
  - reasoning
  - ml
  - systems
categories: systems, ml
giscus_comments: true
related_posts: false
ignore: false
---
Some possibly non-coherent thoughts on decision-making:

Any autonomous system must, by definition, take decisions. It is rational to consider the utility of the decision space and pick a nice point. We draw on our experience and simulate the impact of different decisions in our head, and then we pick one. Is that it?

No, right? Decisions are not irrevocable. You can adapt. If you accidentally oversped, you can apply brakes. 

Predictive decisions rely on implicit or explicit modeling. Models are, in the best case, an nth-order approximation of a complex system, with ideally a decent predictive value and a low residual. Intuition, experience, and wisdom are also just models.

Models are by definition imperfect---a perfect model would also necessitate a perfect simulation of all reality. But they can be, and are, more or less imperfect. We all start off with more imperfect models, and (unless maladaptive) use the residuals from using their predictions to refine them. The decision loop, therefore, may be defined to have these components:

1. Observe inputs, and compute `decision = f(input, intent)`
2. Observe the impact of the decision and compute a course correction if necessary
3. Use the residual to update your hypothesis

Or a more formal attempt:

```python
model: m_init   # Our initial model
intent: i_init  # Some mysterious missing ingredient

while Alive:
  reality = input()
  decision = f(reality, intent, model)
  impact = reality.apply(decision)
  error = intent - impact
  model.update(error)
  intent.update(reality, impact)
```

## What Is An Optimal Decision?
It is tempting to then say that the quality of the initial decision does not matter, because it can always be updated. That models the system as a stochastic process, and is true insofar as that holds/is a reasonable approximation. But that is not the case: human lifetimes are finite and there is a time cost and material cost of bad decisions, there is no recovering from jumping off a cliff, prior actions also affect other agents' models (what we call reputation or trust).

It may then be tempting to say that you want the best model before you take any decisions. But models are by definition updated by taking decisions. Scheduling of decisions is a useful escape hatch/degree of freedom: you may decide to read a book to have a better model before taking a decision with a bigger modeled impact. Scheduling is perhaps a meta-decision: choosing to _explore_ (deferring the big decision) rather than _exploit_.

Deferring is useful insofar as the marginal improvement in your model outweighs the opportunity cost of delaying a decision.  Two examples of instances where deferring is bad:
1. There exists no decision that meaningfully enhances the utility of the deferred decision
2. The opportunity cost of deferment is large

**Connections With Standard Terminology** I think open-loop and closed-loop control in control theory are not appropriate parallels. What I am describing is maybe an adaptive closed-loop system? But an autonomous, adaptive, completely programmable closed-loop system where decisions update both the model and the intent. Or just intelligent and conscious life?
## Why Is This Useful
**How to design systems**. If a system requires some information that is, by definition, not available at bootstrap, adaptive mechanisms are necessary to solve the problem.

**Autonomous intelligence, maybe?** With current ML models, backpropagation is a progressive hypothesis refinement loop, but without an intent. And then model weights are frozen and they are tasked with prediction. But being static, they are not refined, unless we account for periodic batch refinement that is conducted with additional data gathered since the previous run. 

Are models sufficiently adaptive? Is it possible that even with static weights, they learn to simulate memories etc. within those weights? What are the limits of computations that an algorithm running on top of a static machine can express, versus those of an algorithm that can mutate the machine itself?