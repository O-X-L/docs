from datetime import datetime

# pylint: disable=W0622

project = 'OXL - Dokumentation'
copyright = f'{datetime.now().year}, OXL IT Services e.U. (Lizenz: CC BY-NC-ND 4.0)'
author = 'Rath Pascal'
extensions = ['piccolo_theme']
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'piccolo_theme'
html_static_path = ['_static']
master_doc = 'index'
display_version = True
sticky_navigation = True
html_logo = 'https://files.oxl.at/img/oxl3_xs.jpg'
html_favicon = 'https://files.oxl.at/img/oxl3_sm.jpg'
source_suffix = {
    '.rst': 'restructuredtext',
}
html_theme_options = {
    'banner_text': '<a href="https://www.oxl.at">Über OXL</a> | '
                   '<a href="https://blog.o-x-l.at">Blog</a> | '
                   '<a href="https://github.com/O-X-L/docs/issues/new">Fehler melden</a> | '
                   '<a href="https://docs.o-x-l.com" title="Switch to the english version">🇬🇧 English</a>'
}
html_short_title = 'OXL Docs'
html_js_files = ['js/main.js']
html_css_files = ['css/main.css']
