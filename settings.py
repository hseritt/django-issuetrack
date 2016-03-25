''' Settings file for Issuetrack.
'''

from __future__ import absolute_import

import os

APP_NAME='issuetrack'
''' This app's name.
'''

COMMON_DIR='common'
''' The directory for html files used by all main template pages in this app.
'''

PAGE_HEADING_TEMPLATE='page_heading.html'
''' The html file used for the 'top' of all template pages.
'''

FOOT_TEMPLATE='foot.html'
''' The html file used for the 'bottom' of all template pages.
'''

TEMPLATE_DIR='{}'.format(APP_NAME)
''' The subdirectory in the app's template directory. Used to avoid collisions with other app's similarly named template files.
'''

COMMON_TEMPLATES_DIR = os.path.join(TEMPLATE_DIR, COMMON_DIR)
''' Build the relative path to COMMON_DIR.
'''

PAGE_HEADING = os.path.join(COMMON_TEMPLATES_DIR, PAGE_HEADING_TEMPLATE)
''' Build the relative path to PAGE_HEADING_TEMPLATE.
'''

FOOT = os.path.join(COMMON_TEMPLATES_DIR, FOOT_TEMPLATE)
''' Build the relative path to FOOT_TEMPLATE.
'''

TEMPLATE_CONTEXT = {
	'page_heading': PAGE_HEADING,
	'foot': FOOT,
}
''' The standard template context that will be passed on to the application's template files.
	page_heading: 	See PAGE_HEADING
	foot: 			See FOOT
'''