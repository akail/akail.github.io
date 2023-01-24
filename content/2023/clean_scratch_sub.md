Title: Cleaning Scratch Sub-directories
Date: 2023-01-09 00:00
Category: Snippet
Tags: storage,snippets
Authors: Andrew Kail

We recently ran into an issue with a high speed scratch file system after some drive failures.  While the metadata was intact we could not guarantee
that any of the user data was any good.  Since the metadata was good, we could keep the top level user scratch directories intact and remove all other files
under them, saving a bit of time recreating everything.

    find . -maxdepth 2 -mindepth 2 -exec rm -rf {} \;

This snippet should be run with care.
