#!/usr/bin/env bash

gen() {
  fname=what

  while [[ "$fname" != "" ]]; do
    OUT="$(date "+%Y-%m-%d")-$fname.md"
    read -p "Creating file: $OUT. Change? " fname
  done

  echo $fname

  cat > $OUT <<EOF
---
layout: post
title: Some title
date: $(date "+%Y-%m-%d %H:%M:%S%z")
description: Some description
tags: tag
categories: cat
giscus_comments: true
related_posts: false
---
EOF

  echo "Created: $OUT"
}

gen
