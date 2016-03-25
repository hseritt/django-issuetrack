
from __future__ import absolute_import

import os
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from issuetrack.forms import AddIssueForm
from issuetrack.models import Comment, Issue
from issuetrack.settings import TEMPLATE_DIR, TEMPLATE_CONTEXT


def index(request):
	''' View: /
	'''

	view_context = {
		'issue_list': Issue.objects.all(),
		'page_title': 'Issuetracker',
	}
	''' Context used for this view:
		issue_list: 	List of all issues
		page_title: 	Title of the html page
	'''

	view_context.update(TEMPLATE_CONTEXT)
	''' Add standard template context from Issuetrack settings file.
	'''

	template_file = os.path.join(TEMPLATE_DIR, 'index.html')
	''' Template file used by this view.
	'''

	return render(request, template_file, view_context)


def issue(request, issue_id):
	''' View: /issue/<issue_id>/
	'''

	issue = Issue.objects.get(pk=issue_id)
	''' Issue object for this view.
	'''

	view_context = {
		'issue': issue,
		'comment_list': Comment.objects.filter(issue=issue),
		'page_title': 'Issuetrack - Issue #{}'.format(issue.id),
	}
	''' Context used for this view:
		issue: 			Issue object for this view.
		comment_list: 	List of comments for this issue.
		page_title: 	Title of the html page.
	'''

	view_context.update(TEMPLATE_CONTEXT)
	''' Add standard template context from Issuetrack settings file.
	'''

	template_file = os.path.join(TEMPLATE_DIR, 'issue.html')
	''' Template file used by this view.
	'''

	return render(request, template_file, view_context)


def add_issue(request):
	''' View: /issue/add/
	'''

	if request.method == "POST":
		''' If this view is called using the POST method ...
		'''
		
		add_issue_form = AddIssueForm(request.POST)
		''' Get the data from the POST request.
		'''
		
		if add_issue_form.is_valid():
			''' If this is form's data is valid then create the new Issue object.
			'''
			issue = add_issue_form.save(commit=False)
			''' Create the new Issue object but don't commit it to the database just yet. We need to get our user which is not given to us by the form.
			'''
			issue.creater = request.user
			''' Set the issue's creater as the logged in user.
			'''
			issue.save()
			''' Now, save the issue object to peristence.
			'''
			
			return HttpResponseRedirect(reverse('index'))
			''' Send the user back to the "home" page.
			'''

			''' If this form's data is NOT valid, no worries. Django will provide some nice error messages in the generated form.
			'''

	else:
		''' If this view is called by any other method besides POST -- usually 'GET' ...
		'''
		add_issue_form = AddIssueForm()
		''' Create a blank create new issue form.
		'''

	view_context = {
		'add_issue_form': add_issue_form,
		'page_title': 'Issuetrack - Create New Issue',
	}
	''' Context used for this view:
		add_issue_form: 	Our generated add_issue_form.
		page_title: 		Title of the html page.
	'''

	view_context.update(TEMPLATE_CONTEXT)
	''' Add standard template context from Issuetrack settings file.
	'''

	template_file = os.path.join(TEMPLATE_DIR, 'add_issue.html')
	''' Template file used by this view.
	'''
	
	return render(request, template_file, view_context)
