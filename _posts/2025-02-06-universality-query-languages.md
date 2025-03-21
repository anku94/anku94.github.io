---
layout: post
title: On The Universality of Query Languages
date: 2025-02-06 15:08:30
description: Why is SQL what it is? What motivates a different query language?
tags:
  - sql
categories: philosoraptormode
giscus_comments: true
related_posts: false
ignore: false
---
This is an initial quick draft of this line of thought, written 16 hours before a paper deadline I have things to do about (that has nothing to do with query languages). It will be rushed and half-baked, and surreptitiously refined later.

Goal for this post: let us try justifying SQL. Why it exists, why is it in a specific form etc.
## SQL vs Relational Algebra
I think SQL is made-up and non-essential. It is syntactic sugar over relational algebra. Other declarative interfaces may be more convenient abstractions --- I personally prefer dataframes and chaining of expressions.

If you think of the query plan as a dataflow tree leading up to a root, SQL is essentially a traversal over that tree, like in-order, pre-order etc. The order SQL follows, specifically, may be called a _Weird Arbitrary Traversal_ (or _WAT_). That the query planning infra evolved to reflect dataflow is not surprising, data movement is expensive, be it across functions or machines, and the more data you discard closer to the source the better off you are.

These pedantic distinctions are important, because they enable us to reason about 
## On the Universality of Relational Algebra?
Okay so why does relational algebra exist in the form it does?

As a lower bound on this argument, a query interface could just be say... C. You write a blob, machine runs blob, you get output.

We do declarative interfaces to make life easier given certain domain-specific constraints. In the relational world, it is:

1. Leveraging the relational/tabular data model.
2. Leveraging distributed cluster resources.
3. Leveraging fine-grained scheduling, concurrency etc.
4. Getting easy access to indexes etc.
5. Enabling reduced data movement by exposing primitives that capture data flow
6. Enabling query optimization by exposing primitives that make it easier to reason about ordering and statistics
7. Enable reasoning about partitioning and shuffling using key constraints and joins

## Do Relational Operators Do These Things?
To a large extent, yes. That is why relational algebra endures. SQL just pretends to be inseparable from that and most people do not ask too many questions.

You always need escape hatches. That is why UDFs exist. But beyond a point, they hinder the query planning infra's ability to reason about what the blob does.
## Who Deserves To Be In The Club?
What operators should be in this club?
- Can we justify the existence of all existing operators?
- Are there new ones that should be there but are not?
- Under what models do we need radically different solutions?

Relational algebra checks out as it is essentially set theory. Given a table, you can slice it horizontally or vertically. Indexing helps with horizontal slicing. Vertical slicing is harder in row-based stores but column-based stores have solutions. Selection and projection map nicely to dataflow, indexing etc. Division seems to be the only relational operator not directly used in query plans.
## Where Am I Getting At?
There exist data models (such as multidimensional array-based scientific data) that are not relational. Graphs are one example. Nothing here is really new.

The question I am trying to answer is: what is the set of ideas that lead you to the perfect operators for these domains? Do they exist? Are they in conflict with relational algebra?  Or can they be members of the extended family?

_Note to self: read referenced material_ [^1][^2][^3][^4]
## References
[^1]: SciQL, a query language for science applications, Proceedings of the EDBT/ICDT 2011 Workshop on Array Databases, 2011, https://dl.acm.org/doi/10.1145/1966895.1966896
[^2]: MeshSQL: The query language for simulation mesh data, Information Sciences, 2004, https://www.sciencedirect.com/science/article/pii/S0020025503001981
[^3]: Toward unstructured mesh algebra and query language, Proceedings of the 2014 SIGMOD PhD symposium, 2014, https://dl.acm.org/doi/10.1145/2602622.2602626o
[^4]: TileDB ∙ Designed for Discovery, https://tiledb.com/