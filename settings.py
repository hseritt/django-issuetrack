''' Settings file for Issuetrack.
'''

from __future__ import absolute_import

import os

LOGIN_URL='/login/'

APP_NAME='issuetrack'
''' This app's name.
'''

COMMON_TEMPLATES_DIR='common'
''' The directory for html files used by all main template pages in this app.
'''

PAGE_HEADING = 'page_heading.html'
''' The html file used for the 'top' of all template pages.
'''

FOOT = 'foot.html'
''' The html file used for the 'bottom' of all template pages.
'''

FORM_TABLE_HEADING='form_table_heading.html'
''' The html file used for the top of all form tables.
'''

FORM_BUTTONS_HEADING='form_buttons_heading.html'
''' The html file used for the top of all buttons in form tables.
'''

FORM_TABLE_FOOTING = 'form_table_footing.html'
''' The html file used for footing all form tables.
'''

ISSUE_STATUSES = (
	'New',
	'Open',
	'In Progress',
	'Resolved',
	'Closed',
	'On Hold',
	'Pending Creater',
	'Pending 3rd Party',
	'Duplicate',
	'Invalid/Unfounded',
	"Won't Fix",
)

ISSUE_KINDS = (
	'Bug',
	'Improvement',
	'Feature',
	'Info',
	'Proposal',
	'Task',
)

COMMENT_AUDIENCES = (
	'Public',
	'Private',
)

ISSUE_PRIORITIES = (
	'Blocker',
	'Critical',
	'Major',
	'Minor',
	'Trivial',
)

ISSUE_URGENCIES = (
	'ASAP',
	'7 days',
	'21 days',
	'42 days',
	'Indefinite',
)

'''
==================================================
Make settings changes above and leave below as is.
==================================================
'''

TEMPLATE_DIR='{}'.format(APP_NAME)
''' The subdirectory in the app's template directory. Used to avoid collisions with other app's similarly named template files.
'''

COMMON_TEMPLATES_DIR = os.path.join(TEMPLATE_DIR, COMMON_TEMPLATES_DIR)
''' Build the relative path to COMMON_TEMPLATES_DIR.
'''

PAGE_HEADING = os.path.join(COMMON_TEMPLATES_DIR, PAGE_HEADING)
''' Build the relative path to PAGE_HEADING.
'''

FOOT = os.path.join(COMMON_TEMPLATES_DIR, FOOT)
''' Build the relative path to FOOT_TEMPLATE.
'''

FORM_TABLE_HEADING = os.path.join(COMMON_TEMPLATES_DIR, FORM_TABLE_HEADING)
''' Build the relative path to FORM_TABLE_HEADING.
'''

FORM_BUTTONS_HEADING = os.path.join(COMMON_TEMPLATES_DIR, FORM_BUTTONS_HEADING)
''' Build the relative path to FORM_BUTTONS_HEADING.
'''

FORM_TABLE_FOOTING = os.path.join(COMMON_TEMPLATES_DIR, FORM_TABLE_FOOTING)
''' Build the relative path to FORM_TABLE_FOOTING.
'''

TEMPLATE_CONTEXT = {
	'page_heading': PAGE_HEADING,
	'foot': FOOT,
	'form_table_heading': FORM_TABLE_HEADING,
	'form_buttons_heading': FORM_BUTTONS_HEADING,
	'form_table_footing': FORM_TABLE_FOOTING,
}
''' The standard template context that will be passed on to the application's template files.
	page_heading: 		See PAGE_HEADING.
	foot: 				See FOOT.
	form_table_heading: See FORM_TABLE_HEADING.
	form_table_footing: See FORM_TABLE_FOOTING.
'''

# ========================================================

ISSUE_STATUSES = [ (e, e) for e in ISSUE_STATUSES ]

ISSUE_KINDS = [ (e, e) for e in ISSUE_KINDS ]

COMMENT_AUDIENCES = [ (e, e) for e in COMMENT_AUDIENCES ]

ISSUE_PRIORITIES = [ (e, e) for e in ISSUE_PRIORITIES ]

ISSUE_URGENCIES = [ (e, e) for e in ISSUE_URGENCIES ]
''' Build the choices as a two-element list for models and forms.
'''