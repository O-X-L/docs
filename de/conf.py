from datetime import datetime

# pylint: disable=W0622

project = 'OXL - Dokumentation'
copyright = f'{datetime.now().year}, OXL IT Services (Lizenz: CC BY-NC-ND 4.0)'
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
    # 'banner_text': '<a href="https://www.oxl.at">Über OXL</a> | '
    #                '<a href="https://github.com/O-X-L/docs/issues/new">Fehler melden</a> | '
    #                '<a href="https://docs.o-x-l.com" title="Switch to the english version"><img loading="lazy" style="height: 10px; padding: 0; border-radius: 0;" src="https://files.oxl.at/img/flag_gb.svg" alt="England Flag"> English</a>'
    "site_url": "https://docs.OXL.at",
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
        "toc.integrate",
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
                "name": "Zum dunklen Design wechseln",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "deep-orange",
            "accent": "lime",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Zum hellen Design wechseln",
            },
        },
    ],
    "version_dropdown": True,
    "version_info": [
        {
            "version": "https://docs.O-X-L.com",
            "title": "English Manual",
            "aliases": [],
        },
        {
            "version": "https://www.OXL.at",
            "title": "Über OXL",
            "aliases": [],
        },
    ],
    "social": [
        {
            "icon": "fontawesome/solid/globe",
            "link": "https://www.OXL.at",
            "name": "Über OXL",
        },
        {
            "icon": "fontawesome/brands/github",
            "link": "https://github.com/O-X-L",
            "name": "OXL auf GitHub",
        },
    ],
}
html_title = 'OXL Docs'
html_short_title = 'OXL Docs'
html_js_files = ['https://files.oxl.at/js/feedback.js']
html_css_files = ['https://files.oxl.at/css/feedback.css', 'css/main.css']
