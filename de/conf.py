from datetime import datetime

# pylint: disable=W0622

project = 'OXL - Dokumentation'
copyright = f'{datetime.now().year}, OXL'
author = 'OXL'
extensions = ['piccolo_theme']
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'piccolo_theme'
html_static_path = ['_static']
master_doc = 'index'
display_version = True
sticky_navigation = True
html_logo = 'https://files.oxl.at/img/oxl.svg'
html_favicon = 'https://files.oxl.at/img/oxl.svg'
source_suffix = {
    '.rst': 'restructuredtext',
}
html_theme_options = {
    'banner_text': '<a href="https://www.oxl.at">Über OXL</a> | '
                   '<a href="https://github.com/O-X-L/docs/issues/new">Fehler melden</a> | '
                   '<a href="https://docs.o-x-l.com">🇬🇧 Switch to English</a>'
}
html_short_title = 'OXL Docs'
html_js_files = ['js/main.js']
html_css_files = ['css/main.css']
