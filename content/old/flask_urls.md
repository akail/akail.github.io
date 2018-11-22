Title: Building URLs in Flask
Date: 2018-11-30 00:00
Tags:  python, flask
Status: draft

# Introduction

Issue with running flask behind a double layer proxy. Multiple urls were not being generated correctly and certain settings were being ignored

Really describe the problem here.  The goal of this article will be to define the problem and then show how everything flows under the hood and what I can do to fix my particular issue which is definetely a bug/feature of some sort

What are some of the settings that are ignored by the flask configuration?
URL_PREFERRED_SCHEME is ignored

Insert image here of what the architecture looks like

This is an issue with both flask and werkzeug since it handles the underlying routing and url generation

# Building URLs

the url_for function is located in flask in flask.helpers

# Proxy Fix

# Conclusion


