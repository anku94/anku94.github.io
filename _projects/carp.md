---
layout: distill
title: CARP
description: Range Query-Optimized Indexing for Streaming Data.
# img: assets/img/12.jpg
importance: 1
category: work
related_publications: false

authors:
  - name: Ankush Jain
    url: ""
    affiliations:
      name: CMU
  - name: Charles D. Cranor
    url: ""
    affiliations:
      name: CMU
  - name: Qing Zheng
    url: ""
    affiliations:
      name: LANL
  - name: Bradley W. Settlemeyer
    url: ""
    affiliations:
      name: Nvidia
  - name: George Amvrosiadis
    url: ""
    affiliations:
      name: CMU
  - name: Gary A. Grider
    url: ""
    affiliations:
      name: LANL

bibliography: carp.bib
---

This is a brief description of CARP <d-cite key="Jain2024:CARP" /> , 
which was (eventually) published to Supercomputing 2024. [PDF here]({{ "/assets/pdf/carp.pdf" | relative_url }}), and [code here]({{ "https://github.com/pdlfs/carp-umbrella" }}).

With CARP, we wanted to speed up ingestion of data from large parallel apps for range query indexing. Current approaches re-read data from the parallel filesystem, reprocess it, and write it back. These applications are $$ O(100K)$$ cores, and generate large amounts of data. Postprocessing costs valuable time and hardware resources.

In-situ indexing is a popular alternative. In-situ partitioning, which in my opinion is the king of in-situ indexing systems, currently does not work for range queries --- CARP fixes that. Range queries like locality in their data layouts. A bulk sort maximizes data locality, but at significant I/O cost. CARP approximates this using a streaming pipeline.

CARP is essentially a greedy single-pass partial sorter. To preserve I/O cycles, we choose not to reorder data for perfect partitioning, but instead choose to compromise on the sortedness instead. This works really well --- CARP queries are almost as fast as a full sort, but without any ingestion overhead (making CARP $$5\times$$ faster than the state-of-the-art).

## What is Missing

CARP is a tool in an analysis toolkit --- it requires setting up, knowing when to use the CARP index, how to configure CARP etc.

These aspects significantly limit the adoption of advanced techniques by scientific data users. Databases have been working on this problem for ages --- they expose a uniform interface (SQL), and smart query plans are able to transparently do The Best Thing<sup>TM</sup>. We need equivalents for scientific data analyses, and ways to incorporate techniques like approximate indices into their toolkits.
