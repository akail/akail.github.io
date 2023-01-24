Title: Github Action to Publish Pelican
Date: 2101-01-01 12:00
Category: Projects
Tags: github,pelican
Authors: Andrew Kail


As I set out to start this blog I was interested in automating the deployment to my
github page by using Github actions with Pelican, the static site generator I use
to make this website. I am also a personal fan of [poetry](https://python-poetry.org)
for managing my python projects and their dependencies so will be using that here.

This github action will do the folowing steps.

1. Checkout my repository and theme
2. Install python, poetry, and all my dependencies
3. Install the theme
4. Install the pygments style for syntax highlighting
5. Build the static website
6. Push the changes to the gh-pages branch

Below is the full github action with inline notes:

    :::yaml
    name: deploy-site

    # Only run this when the master branch changes
    on:
      push:
        branches:
        - master

    # This job installs dependencies, builds the book, and pushes it to `gh-pages`
    jobs:
      deploy-book:
        runs-on: ubuntu-latest
        steps:
        
        # Checkout this repository
        - name: Checkout this repository
          uses: actions/checkout@v2

        # Checkout external theme in a nested directory
        - name: Checkout Flex theme
          uses: actions/checkout@v3
          with:
            repository: 'alexandrevicenzi/Flex'
            path: Flex

        # Install Python
        - name: Set up Python 3.10
          uses: actions/setup-python@v4
          with:
            python-version: "3.10"

        # Install poetry
        - name: Install poetry
          run: pip install poetry

        # Install poetry dependencies, but do not attempt to install a root package
        # (See poetry docs for details on --no-root)
        - name: Install dependencies
          run: poetry install --no-root

        # Install the theme from the Flex repository
        - name: Install theme
          run: poetry run pelican-themes -i Flex

        # Generate missing css for syntax highlighting
        - name: Generate pygments css
          run: poetry run pygmentize -S gruvbox-dark -f html -a .highlight > output/theme/pygments/gruvbox-dark.min.css

        # Generate static website using the invoke tool
        - name: Build the website
          run: poetry run invoke preview

        # Push the book's HTML to github-pages
        - name: GitHub Pages action
          uses: peaceiris/actions-gh-pages@v3.6.1
          with:
            github_token: ${{ secrets.GITHUB_TOKEN }}
            publish_dir: ./output
            cname: blog.kail.io

            
I use this to update items I need updated immediately, like new pages, corrections, or modifications to existing articles.  This however does not handle the daily updates for future articles to get published day of.  For that you can add a new directive to define a scheduled cronjob.

    :::yaml
    on:
      push:
        branches:
          - master
      schedule:
        - cron: '45 8 * * * '

This will now run each day at 8:45 AM to regenerate the website and publish new articles if they are available.  I will actually be splitting
