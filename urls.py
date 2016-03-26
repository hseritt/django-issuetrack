from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

from issuetrack.views import index, issue, add_issue, add_project, projects, project, add_component

urlpatterns = [
    url(
        regex=r'^logout/$', 
        view=logout, 
        kwargs={'next_page': '/issuetrack/'}, 
        name='logout'
    ),
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
    url(
        regex=r'^projects/$',
        view=projects,
        name='projects',
    ),
    url(
        regex=r'^project/add/$',
        view=add_project,
        name='add_project',
    ),
    url(
        regex=r'^project/(?P<project_id>[^/]+)/$',
        view=project,
        name='project',
    ),
    url(
        regex=r'^project/(?P<project_id>[^/]+)/component/add/$',
        view=add_component,
        name='add_component',
    ),
]