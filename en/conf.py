from datetime import datetime

# pylint: disable=W0622

project = 'OXL - Documentation'
copyright = f'{datetime.now().year}, OXL IT Services (License: CC BY-NC-ND 4.0)'
author = 'Rath Pascal'
extensions = ['sphinx_immaterial']
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'sphinx_immaterial'
html_static_path = ['_static']
master_doc = 'index'
display_version = True
sticky_navigation = True
html_logo = 'https://files.oxl.at/img/oxl3_xst.webp'
html_favicon = 'https://files.oxl.at/img/oxl3_sm.webp'
source_suffix = {
    '.rst': 'restructuredtext',
}
html_theme_options = {
    # 'banner_text': '<a href="https://www.o-x-l.com">About OXL</a> | '
    #                '<a href="https://github.com/O-X-L/docs/issues/new">Report errors</a> | '
    #                '<a href="https://docs.oxl.at" title="Zur deutschsprachigen Version wechseln"><img loading="lazy" style="height: 10px; padding: 0; border-radius: 0;" src="https://files.oxl.at/img/flag_de.svg" alt="German Flag"> Deutsch</a>'
    "site_url": "https://docs.O-X-L.com",
    "repo_url": "https://github.com/O-X-L/docs",
    "repo_name": "OXL Docs",
    "globaltoc_collapse": True,
    "features": [
        "navigation.expand",
        # "navigation.tabs",
        # "navigation.tabs.sticky",
        # "toc.integrate",
        "navigation.sections",
        # "navigation.instant",
        # "header.autohide",
        "navigation.top",
        "navigation.footer",
        # "navigation.tracking",
        # "search.highlight",
        "search.share",
        "search.suggest",
        "toc.follow",
        "toc.sticky",
        "content.tabs.link",
        "content.code.copy",
        "content.action.edit",
        "content.action.view",
        "content.tooltips",
        "announce.dismiss",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "light-blue",
            "accent": "light-green",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to dark-mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "deep-orange",
            "accent": "lime",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to light-mode",
            },
        },
    ],
    "version_dropdown": True,
    "version_info": [
        {
            "version": "https://docs.OXL.at",
            "title": "Deutsches Handbuch",
            "aliases": [],
        },
        {
            "version": "https://www.O-X-L.com",
            "title": "About OXL",
            "aliases": [],
        },
    ],
    "social": [
        {
            "icon": "fontawesome/solid/globe",
            "link": "https://www.O-X-L.com",
            "name": "About OXL",
        },
        {
            "icon": "fontawesome/brands/github",
            "link": "https://github.com/O-X-L",
            "name": "OXL on GitHub",
        },
    ],
}
html_title = 'OXL Docs'
html_short_title = 'OXL Docs'
html_js_files = ['https://files.oxl.at/js/feedback.js']
html_css_files = ['https://files.oxl.at/css/feedback.css', 'css/main.css']
