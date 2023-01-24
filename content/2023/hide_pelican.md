Title: Hide Pelican Articles on Output
Date: 2023-01-02 00:00
Category: Python
Tags: pelican

Authors: Andrew Kail

While working on this website I had started to draft a lot of articles in preparation
to develop some consistency and start to flesh out a book on [HPC](https://hpc.kail.io).

In doing so, I found that there was no way to prevent these articles from being generated and could be
accessed by anyone digging through the site or my github repository.  While not a big deal since the drafts
themselves exist as markdown files, I wanted to keep the published website clean and began looking for a way
to clean things up.

Pelican offers a few ways to control what gets generated on your website.  The first is by using the "Status" metadata
tag on an article or page.  The status can be draft, hidden, or published.  If an article is in draft, it will be listed under
the drafts directory of the web page.  If the article is hidden, it will be generated under the root directory as normal,
but will not have any links to it via tags or categories.  Published means the article is published.

No matter which status we chose, the html for the article will be generated.

There have been a few [attempts](https://github.com/getpelican/pelican/issues/1965) at adding this feature, but
no one has stepped forward to implement it unfortunately.  From reading this issue the simplest solution is to leverage the `IGNORE_FILES` setting
in `publishconf.py` and move all drafts to a sub-folder in the `content` directory. `IGNORE_FILES` takes a list of regular
expressions one can use to exclude files and directories from generation.  For example, I created a directory `drafts`
and moved all my draft files under there, and then kept my published files under a year based structure.  To exclude
files in the drafts folder and maintain the pelican defaults, the following should be added:

```python
IGNORE_FILES = [".#*", "drafts"]
```

Now to ensure that all files under the drafts directory have the appropriate statue, we set `EXTRA_PATH_METADATA`
in `pelicanconf.py` to set the default status.


```python
EXTRA_PATH_METADATA = {
    "drafts": {"status": "draft"},
}
```

This will ensure drafts do not accidently populate the post list while developing and reduce the extra step of 
setting the status.
