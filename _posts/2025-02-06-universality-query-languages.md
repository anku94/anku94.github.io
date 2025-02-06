---
layout: post
title: On The Universality of Query Languages
date: 2025-02-06 15:08:30
description: Why is SQL what it is? What motivates a different query language?
tags:
  - tag
categories: cat
giscus_comments: true
related_posts: false
ignore: false
---
This is an initial quick draft of this line of thought, written 16 hours before a paper deadline I have things to do about (that has nothing to do with query languages). It will be rushed and half-baked, and surreptitiously refined later.

Goal for this post: let us try justifying SQL. Why it exists, why is it in a specific form etc.
## SQL vs Relational Algebra
I think SQL is made-up and non-essential. It is syntactic sugar over relational algebra. Other declarative interfaces may be more convenient abstractions --- I personally prefer dataframes and chaining of expressions.
## On the Universality of Relational Algebra?
Okay so why does relational algebra exist in the form it does?

As a lower bound on this argument, a query interface could just be say... C. You write a blob, machine runs blob, you get output.

We do declarative interfaces to make life easier given certain domain-specific constraints. In the relational world, it is:

1. Leveraging the relational/tabular data model 
2. Leveraging distributed cluster resources
3. Leveraging fine-grained scheduling
4. Getting easy access to indexes etc.
5. Enabling reduced data movement by exposing primitives that capture data flow
6. Enabling query optimization by exposing primitives that make it easier to reason about ordering and statistics
7. Something about partitioning and shuffling that is probably covered in the previous examples
## Do Relational Operators Do These Things?
To a large extent, yes. That is why relational algebra endures. SQL just pretends to be inseparable from that and most people do not ask too many questions.

You always need escape hatches. That is why UDFs exist. But beyond a point, they hinder the query planning infra's ability to reason about what the blob does.
## Who Deserves To Be In The Club?
What operators should be in this club?
- Can we justify the existence of all existing operators?
- Are there new ones that should be there but are not?
- Under what models do we need radically different solutions?

Let's start with a table. Rows and columns. You can slice it horizontally or vertically. Indexing helps with horizontal slicing. Vertical slicing is harder in row-based stores but column-based stores have solutions. Selection and projection map nicely to dataflow, indexing etc.
## Where Am I Getting At?
There exist data models (such as multidimensional array-based scientific data) that are not relational. Graphs are one example. Nothing here is really new.

The question I am trying to answer is: what is the set of ideas that lead you to the perfect operators for these domains? Do they exist? Are they in conflict with relational algebra?  Or can they be members of the extended family?

_To be continued..._
