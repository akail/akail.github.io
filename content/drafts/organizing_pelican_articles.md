Title: Organizing Pelican Articles
Date: 2101-01-01 12:00
Category: HPC
Tags: hpc,slurm
Authors: Andrew Kail

My plan for 2023 is to write a blog post a week, which would amount to 52 articles!  For this blog,
I am using [Pelican](https://getpelican.com), a tool I have used before to genereate static HTML websites. 


Pelican puts files
Since this will be a lot of markdown files in a single directory


    .
    ├── content
    │   ├── clean_scratch_sub.md
    │   ├── extra
    │   │   └── custom.css
    │   ├── hide_pelican.md
    │   ├── images
    │   │   ├── Andrew2018.jpg
    │   │   └── profile.png
    │   ├── opensense_to_proxmox_1.md
    │   ├── opensense_to_proxmox_2.md
    │   ├── organizing_pelican_articles.md
    │   ├── pages
    │   │   ├── about.md
    │   │   ├── contact.md
    │   │   └── projects.md
    │   └── pelican_github_action.md
    ├── output
    ├── pelicanconf.py
    ├── poetry.lock
    ├── publishconf.py
    ├── pyproject.toml
    └── tasks.py

Most of the articles are one level deep under the `content` directory and if I continue the pace
of writing that I have setup for myself, it will become very crowded and difficult to read.  Instead I
would like to organize the articles by year.
