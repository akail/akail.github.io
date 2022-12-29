AUTHOR = 'Andrew Kail'
SITENAME = "Andrew Kail's Blog"
SITEURL = ''
SITETITLE = "Andrew Kail"
SITESUBTITLE = "Somewhat HPC related blog"
SITELOGO = SITEURL + "/images/profile.png"

PATH = 'content'

TIMEZONE = 'US/Eastern'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'https://getpelican.com/'),
         # ('Python.org', 'https://www.python.org/'),
         # ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         # ('You can modify those links in your config file', '#'),)
LINKS = (("My Configs", "https://github.com/akail/Configs"),
         ('HPC Book (WIP)', 'https://hpc.kail.io'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Theme settings
THEME = 'Flex'
THEME_COLOR = "light"
PYGMENTS_STYLE = "gruvbox-dark"
STATIC_PATHS = ["extra/custom.css", "images"]

EXTRA_PATH_METADATA = {
    "extra/custom.css": {"path": "static/custom.css"},
}
CUSTOM_CSS = "static/custom.css"

CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike",
    "version": "4.0",
    "slug": "by-sa"
}

# Menu configurations
MAIN_MENU = True

SOCIAL = (
    ("github", "https://github.com/akail"),
    ("rss", "/feeds/all.atom.xml"),
    ("linkedin", "https://www.linkedin.com/in/andrewkail/"),
    ("mastodon", "https://fosstodon.org/@akail")
)

MENUITEMS = (
    ("Archives", "/archives.html"),
    ("Categories", "/categories.html"),
    ("Tags", "/tags.html"),
)

DEFAULT_METADATA = {
    'status': 'draft',
}

