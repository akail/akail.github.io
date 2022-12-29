Title: Hide Pelican Articles on Output
Date: 2022-12-29 12:00
Category: Python
Tags: pelican
Status: published

Authors: Andrew Kail

While working on this website I had started to draft a lot of articles in preparation
to develop some consistency and start to flesh out a book on [HPC](https://hpc.kail.io).

In doing so, I found that there was no way to prevent these articles from being generated and could be
accessed by anyone digging through the site or my github repository.  While not a big deal since the drafts
themselves exist as markdown files, I wanted to keep the website out clean and began looking at how to clean things up.

Pelican offers a few ways to control what gets generated on your website.  The first is by using the "Status" metadata
tag on an article or page.  The status can be draft, hidden, or published.  If an article is in draft, it will be listed under
the drafts directory of the web page.  If the article is hidden, it will be generated under the root directory as normal,
but will not have any links to it via tags or categories.  Published means the article is published.  

No matter which status we chose, the html for the article will be generated regardless. 

There have been a few [attempts](https://github.com/getpelican/pelican/issues/1965) at adding this feature, but
no one has stepped forward.  From reading this issue the simplest solution is to leverage the `IGNORE_FILES` setting
in `publishconf.py` and adding some syntactical sugar to our file naming convention. `IGNORE_FILES` takes a list of regular
expressions one can use to exclude files from generation.  What we will do here is tell Pelican to ignore markdown files with the word
"unpublished" in its name.


    :::python
    IGNORE_FILES = ["*unpublished*.md"]

You can now rename any files you don't want published to include "unpublished". Now when developing, those files will still be generated, but when publishing, will be ignored.
