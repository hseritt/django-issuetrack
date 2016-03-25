from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

from issuetrack.views import index, issue, add_issue

urlpatterns = [
    url(
    	regex=r'^$',
    	view=index,
    	name='index'
    ),
    url(
    	regex=r'^issue/add/$',
    	view=add_issue,
    	name='add_issue',
    ),
    url(
		regex=r'^issue/(?P<issue_id>[^/]+)/$',
		view=issue,
		name='issue',
	),
]