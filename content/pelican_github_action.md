Title: Github Action to Publish Pelican
Date: 2101-01-01 12:00
Category: Projects
Status: draft
Tags: github,pelican
Authors: Andrew Kail

What the title says


    :::yaml
    name: deploy-site

    # Only run this when the master branch changes
    on:
      push:
        branches:
        - master
        # If your git repository has the Jupyter Book within some-subfolder next to
        # unrelated files, you can make this run only if a file within that specific
        # folder has been modified.
        #
        # paths:
        # - some-subfolder/**

    # This job installs dependencies, builds the book, and pushes it to `gh-pages`
    jobs:
      deploy-book:
        runs-on: ubuntu-latest
        steps:
        - name: Checkout this repository
          uses: actions/checkout@v2

        - name: Checkout Flex theme
          uses: actions/checkout@v3
          with:
            repository: 'alexandrevicenzi/Flex'
            path: Flex

        # Install dependencies
        - name: Set up Python 3.10
          uses: actions/setup-python@v4
          with:
            python-version: "3.10"

        - name: Install poetry
          run: pip install poetry

        - name: Install dependencies
          run: poetry install --no-root

        - name: Install theme
          run: poetry run pelican-themes -i Flex

        - name: Generate pygments css
          run: poetry run pygmentize -S gruvbox-dark -f html -a .highlight > output/theme/pygments/gruvbox-dark.min.css

        # Build the book
        - name: Build the book
          run: poetry run invoke preview

        # Push the book's HTML to github-pages
        - name: GitHub Pages action
          uses: peaceiris/actions-gh-pages@v3.6.1
          with:
            github_token: ${{ secrets.GITHUB_TOKEN }}
            publish_dir: ./output
            cname: blog.kail.io