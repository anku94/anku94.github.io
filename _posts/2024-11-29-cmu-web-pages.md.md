---
layout: post
title: Notes on Web Pages and CMU Infra
date: 2024-11-29 13:11:12-0500
description: Dealing with AFS, cells, permissions etc.
tags:
  - web
categories: web
giscus_comments: true
related_posts: false
---
Infra for hosting web pages on CMU web servers is a little complicated and confusing, and I waste some time figuring it out every time I need to change something. These are notes to make my life easier in the future, and may be relevant for others. This is from the perspective of an ECE student, adapt to your needs.

## AFS Cells
I get to have a home directory on two CMU cells -- `andrew.cmu.edu` and `ece.cmu.edu`. I don't know how to discover all the cells you have a home directory in.

```
ssh ankushj@unix.andrew.cmu.edu # give them your andrew password
$ pwd
/afs/andrew.cmu.edu/usr18/ankushj
$ cd /afs/ece.cmu.edu/usr/ankushj
$ ls
Permission denied
$ aklog ece.cmu.edu
$ ls
top_secret_infiniband_content.txt
$ tokens
<all the cells I'm authenticated for>

# random AFS commands
$ fs listaliases
$ fs listquota
```

## Hosting on ECE
This is straightforward. Your `public_html` is available on `users.ece.cmu.edu/~ankushj`

ECE also respects `.htaccess`

```
$ ls -a /path/to/ece/homedir/public_html
.htaccess index.html
```

## Hosting on Andrew
This is more confusing. Target address is `https://www.andrew.cmu.edu/user/ankushj/`.

```
$ ls -a /path/to/andrew/homedir/www
.htaccess index.html
```

1. Andrew does not use `.htaccess`.
2. `index.html` is not automatically available. You have to go to `https://www.andrew.cmu.edu/server/publish.html`, type your username, hit publish, and the data gets copied to some "real hosting destination".
3. `.unpublish` is a thing[^1]

## Redirects
On ECE, I can set up a HTTP-level redirect via `.htaccess`.
```
RedirectMatch 301 ^/$ https://my.real.website
```

I previously tried the following, but it would redirect to `https://my.real.website~ankushj`. I am pretty sure that ChatGPT is just giving me a stupid redirect command, but the version above works and the version below does not --- that'll have to do for now.
```
Redirect 301 / https://my.real.website
```

From Andrew, I had to set up a HTTP redirect.
```
<!DOCTYPE html>
<html>
  <head>
        <meta http-equiv="refresh" content="0; url=https//my.real.website">
            <title>Redirecting...</title>
  </head>
  <body>
        <p>If you are not redirected, <a href="https://my.real.website">click here</a>.</p>
  </body>
</html>
```
## Troubleshooting
```
# Permissions
$ fs sa www system:anyuser rl
```

## References
[^1]: https://www.cmu.edu/computing/services/comm-collab/websites/user-course-web/how-to/publish.html