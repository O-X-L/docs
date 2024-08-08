from datetime import datetime

# pylint: disable=W0622

project = 'OXL - Documentation'
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
html_logo = '_static/img/oxl.svg'
html_favicon = 'img/oxl.svg'
source_suffix = {
    '.rst': 'restructuredtext',
}
html_theme_options = {
    'banner_text': '<a href="https://www.o-x-l.com">About OXL</a> | '
                   '<a href="https://github.com/O-X-L/docs/issues/new">Report errors</a> | '
                   '<a href="https://docs.oxl.at">🇩🇪 Zu Deutsch wechseln</a>'
}
html_short_title = 'OXL Docs'
html_js_files = ['js/main.js']
html_css_files = ['css/main.css']
