
from __future__ import absolute_import

import os
from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from issuetrack.forms import AddIssueForm, AddProjectForm, AddComponentForm
from issuetrack.forms import AddCommentForm, ChangeIssueForm, ChangeCommentForm
from issuetrack.forms import ChangeProjectForm, ChangeComponentForm
from issuetrack.models import Comment, Component, Issue, Project
from issuetrack.settings import TEMPLATE_DIR, TEMPLATE_CONTEXT, LOGIN_URL


@login_required(login_url=LOGIN_URL)
def index(request):
    ''' View: /
    '''

    default_sort_order = 'created'
    ''' This view's default sorting order in lieu of a valid order field.
    '''
    order = request.GET.get('order_by', default_sort_order)
    ''' Requested sorting order for this view.
    '''
    status = request.GET.get('status', 'all')
    ''' Filter by status or use 'all'.
    '''

    if request.user.is_staff or request.user.is_superuser:
        kwargs = {}
    else:
        kwargs = {'creater': request.user}
    ''' Staff and superuser users can see all available issues. Non-privileged
     users can only see their own issues.
    '''

    try:

        if status == 'all':
            issue_list = list(Issue.objects.filter(**kwargs).order_by(order))
        elif status == 'open':
            issue_list = list(Issue.objects.filter(**kwargs).exclude(
                status='Closed').order_by(order))
        elif status == 'closed':
            issue_list = list(
                Issue.objects.filter(
                    **kwargs, status='Closed').order_by(order))

    except FieldError:

        if status == 'all':
            issue_list = list(
                Issue.objects.filter(**kwargs).order_by(default_sort_order))
        elif status == 'open':
            issue_list = list(
                Issue.objects.filter(**kwargs).exclude(
                    status='Closed').order_by(default_sort_order))
        elif status == 'closed':
            issue_list = list(
                Issue.objects.filter(
                    **kwargs, status='Closed').order_by(default_sort_order))

    paginator = Paginator(issue_list, 25)
    page = request.GET.get('page')

    try:
        issue_list = paginator.page(page)
    except PageNotAnInteger:
        issue_list = paginator.page(1)
    except EmptyPage:
        issue_list = paginator.page(paginator.num_pages)

    view_context = {
        'issue_list': issue_list,
        'page_title': 'Issuetrack',
        'status': status,
    }
    ''' Context used for this view:
        issue_list:     List of all issues
        page_title:     Title of the html page
    '''

    view_context.update(TEMPLATE_CONTEXT)
    ''' Add standard template context from Issuetrack settings file.
    '''

    template_file = os.path.join(TEMPLATE_DIR, 'index.html')
    ''' Template file used by this view.
    '''

    return render(request, template_file, view_context)


@login_required(login_url=LOGIN_URL)
def projects(request):
    ''' View: /projects/
    '''

    view_context = {
        'project_list': Project.objects.all(),
        'page_title': 'Issuetrack - Projects',
    }
    ''' Context used for this view:
        projects_list:  List of all projects
        page_title:     Title of the html page
    '''

    view_context.update(TEMPLATE_CONTEXT)
    ''' Add standard template context from Issuetrack settings file.
    '''

    template_file = os.path.join(TEMPLATE_DIR, 'projects.html')
    ''' Template file used by this view.
    '''

    return render(request, template_file, view_context)


@login_required(login_url=LOGIN_URL)
def issue(request, issue_id):
    ''' View: /issue/<issue_id>/
    '''

    issue = Issue.objects.get(pk=issue_id)
    ''' Issue object for this view.
    '''

    if request.user != issue.creater and not request.user.is_superuser and \
    not request.user.is_staff:
        return HttpResponseRedirect(reverse('index'))
    ''' Only staff, issue owners and superuser users can see their
    issue details.
    '''

    view_context = {
        'issue': issue,
        'comment_list': Comment.objects.filter(issue=issue),
        'page_title': 'Issuetrack - Issue #{}'.format(issue.id),
    }
    ''' Context used for this view:
        issue:          Issue object for this view.
        comment_list:   List of comments for this issue.
        page_title:     Title of the html page.
    '''

    view_context.update(TEMPLATE_CONTEXT)
    ''' Add standard template context from Issuetrack settings file.
    '''

    template_file = os.path.join(TEMPLATE_DIR, 'issue.html')
    ''' Template file used by this view.
    '''

    return render(request, template_file, view_context)


@login_required(login_url=LOGIN_URL)
def project(request, project_id):
    ''' View: /project/<project_id>/
    '''

    project = Project.objects.get(pk=project_id)
    ''' Project object for this view.
    '''

    view_context = {
        'project': project,
        'page_title': 'Issuetrack - Project: {}'.format(project.name),
    }
    ''' Context used for this view:
        project:        Project object for this view.
        page_title:     Title of the html page.
    '''

    view_context.update(TEMPLATE_CONTEXT)
    ''' Add standard template context from Issuetrack settings file.
    '''

    template_file = os.path.join(TEMPLATE_DIR, 'project.html')
    ''' Template file used by this view.
    '''

    return render(request, template_file, view_context)


@login_required(login_url=LOGIN_URL)
def add_issue(request):
    ''' View: /issue/add/
    '''

    if request.method == "POST":
        ''' If this view is called using the POST method ...
        '''

        add_issue_form = AddIssueForm(request.POST, user=request.user)
        ''' Get the data from the POST request.
        '''

        if add_issue_form.is_valid():
            ''' If this is form's data is valid then create the new
            Issue object.
            '''
            issue = add_issue_form.save(commit=False)
            ''' Create the new Issue object but don't commit it to
            the database just yet. We need to get our user which is not
            given to us by the form.
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

            ''' If this form's data is NOT valid, no worries. Django
            will provide some nice error messages in the generated form.
            '''

    else:
        ''' If this view is called by any other method besides POST --
        usually 'GET' ...
        '''
        add_issue_form = AddIssueForm(user=request.user)
        ''' Create a blank create new issue form.
        '''

    view_context = {
        'add_issue_form': add_issue_form,
        'page_title': 'Issuetrack - Create New Issue',
    }
    ''' Context used for this view:
        add_issue_form:     Our generated add_issue_form.
        page_title:         Title of the html page.
    '''

    view_context.update(TEMPLATE_CONTEXT)
    ''' Add standard template context from Issuetrack settings file.
    '''

    template_file = os.path.join(TEMPLATE_DIR, 'add_issue.html')
    ''' Template file used by this view.
    '''

    return render(request, template_file, view_context)


@login_required(login_url=LOGIN_URL)
def add_project(request):
    ''' View: /project/add/
    '''

    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseRedirect(
            reverse('projects')
        )
    ''' Only staff and superuser users can create projects.
    '''

    if request.method == 'POST':
        ''' If this view is called using the POST method ...
        '''

        add_project_form = AddProjectForm(request.POST)
        ''' Get the data from the POST request.
        '''

        if add_project_form.is_valid():
            ''' If this is form's data is valid then create the new
            Issue object.
            '''
            add_project_form.save()
            ''' Save the Project object to peristence.
            '''
            return HttpResponseRedirect(
                reverse('projects')
            )
            ''' Redirect to the "home" page.
            '''
    else:
        ''' If this view is called by any other method besides POST --
        usually 'GET' ...
        '''
        add_project_form = AddProjectForm()
        ''' Create a blank project form.
        '''

    view_context = {
        'add_project_form': add_project_form,
        'page_title': 'Issuetrack - Add New Project',
    }

    view_context.update(TEMPLATE_CONTEXT)
    ''' Add standard template context from Issuetrack settings file.
    '''

    template_file = os.path.join(TEMPLATE_DIR, 'add_project.html')
    ''' Template file used by this view.
    '''

    return render(request, template_file, view_context)


@login_required(login_url=LOGIN_URL)
def add_component(request, project_id):
    ''' View: /project/<project_id>/component/add/
    '''

    project = Project.objects.get(pk=project_id)
    ''' Project object this component is being added for.
    '''

    if not request.user.is_staff and not request.user.is_superuser and \
    project.owner != request.user:
        return HttpResponseRedirect(
            reverse('project', kwargs={'project_id': project_id})
        )
    ''' Only staff users, project owners and superuser users can add
    a component to a project.
    '''

    if request.method == 'POST':
        ''' If this view is called using the POST method ...
        '''

        add_component_form = AddComponentForm(request.POST)
        ''' Get the data from the POST request.
        '''

        if add_component_form.is_valid():
            ''' If this is form's data is valid then create the new
            Component object.
            '''

            new_component = add_component_form.save(commit=False)
            ''' Create the new component for the project but don't save it yet.
            '''
            new_component.project = project
            ''' Set the project.
            '''
            new_component.save()
            ''' Save the new component to persistence.
            '''

            return HttpResponseRedirect(
                reverse(
                    'project', kwargs={'project_id': project_id}
                )
            )
            ''' Redirect the user to individual project page.
            '''
    else:
        add_component_form = AddComponentForm()
        ''' Create an empty component form.
        '''

    view_context = {
        'add_component_form': add_component_form,
        'page_title': 'Issuetrack - Add New Component for Project {}'.format(
            project_id),
        'project': project,
    }
    ''' Context used for this view:
        add_component_form:     Generated AddComponentForm.
        page_title:             Title of the html page.
        project:                Project object for this view.
    '''

    view_context.update(TEMPLATE_CONTEXT)
    ''' Add standard template context from Issuetrack settings file.
    '''

    template_file = os.path.join(TEMPLATE_DIR, 'add_component.html')
    ''' Template file used by this view.
    '''

    return render(request, template_file, view_context)


@login_required(login_url=LOGIN_URL)
def add_comment(request, issue_id):
    ''' View: /issue/<issue_id>/comment/add/
    '''

    issue = Issue.objects.get(pk=issue_id)
    ''' Issue object this comment is being added for.
    '''

    if not request.user.is_staff and not request.user.is_superuser and \
    issue.creater != request.user:
        return HttpResponseRedirect(
            reverse('index')
        )
    ''' Only staff, issue owners and superuser users can add a comment to
    an issue.
    '''

    if request.method == 'POST':
        ''' If this view is called using the POST method ...
        '''

        add_comment_form = AddCommentForm(request.POST)
        ''' Get the data from the POST request.
        '''

        if add_comment_form.is_valid():
            ''' If this is form's data is valid then create the new
            Component object.
            '''

            new_comment = add_comment_form.save(commit=False)
            ''' Create the new comment for the issue but don't save it yet.
            '''
            new_comment.issue = issue
            ''' Set the issue.
            '''
            new_comment.author = request.user
            ''' Set the author of the comment based on the logged-in user.
            '''

            issue.status = add_comment_form.cleaned_data['status']
            issue.save()

            new_comment.issue_status = issue.status

            new_comment.save()
            ''' Save the new component to persistence.
            '''

            return HttpResponseRedirect(
                reverse(
                    'issue', kwargs={'issue_id': issue_id}
                )
            )
            ''' Redirect the user to individual issue page.
            '''
    else:
        add_comment_form = AddCommentForm(issue_status=issue.status)
        ''' Create an empty comment form.
        '''

    view_context = {
        'add_comment_form': add_comment_form,
        'page_title': 'Issuetrack - Add New Comment for Issue {}'.format(
            issue_id),
        'issue': issue,
    }
    ''' Context used for this view:
        add_comment_form:   Generated AddCommentForm.
        page_title:             Title of the html page.
        issue:              Issue object for this view.
    '''

    view_context.update(TEMPLATE_CONTEXT)
    ''' Add standard template context from Issuetrack settings file.
    '''

    template_file = os.path.join(TEMPLATE_DIR, 'add_comment.html')
    ''' Template file used by this view.
    '''

    return render(request, template_file, view_context)


@login_required(login_url=LOGIN_URL)
def change_issue(request, issue_id):
    ''' View: /issue/<issue_id>/change/
    '''

    issue = Issue.objects.get(pk=issue_id)

    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseRedirect(
            reverse('issue', kwargs={'issue_id': issue_id})
        )

    if request.method == "POST":
        ''' If this view is called using the POST method ...
        '''

        change_issue_form = ChangeIssueForm(request.POST, instance=issue)
        ''' Get the data from the POST request but saving for this issue.
        '''

        if change_issue_form.is_valid():
            ''' If this is form's data is valid then create the new
            Issue object.
            '''
            issue = change_issue_form.save()
            ''' Save data from this form to the same issue.
            '''

            return HttpResponseRedirect(reverse(
                'issue', kwargs={'issue_id': issue.id}))
            ''' Send the user back to the issue's page.
            '''

    else:
        ''' If this view is called by any other method besides POST --
        usually 'GET' ...
        '''
        change_issue_form = ChangeIssueForm(instance=issue)
        ''' Create a change issue form based on the issue instance.
        '''

    view_context = {
        'change_issue_form': change_issue_form,
        'page_title': 'Issuetrack - Change Issue - {}'.format(issue.id),
    }
    ''' Context used for this view:
        change_issue_form:  Our generated change_issue_form.
        page_title:         Title of the html page.
    '''

    view_context.update(TEMPLATE_CONTEXT)
    ''' Add standard template context from Issuetrack settings file.
    '''

    template_file = os.path.join(TEMPLATE_DIR, 'change_issue.html')
    ''' Template file used by this view.
    '''

    return render(request, template_file, view_context)


@login_required(login_url=LOGIN_URL)
def change_comment(request, comment_id):
    ''' View: /comment/<comment_id>/change/
    '''

    comment = Comment.objects.get(pk=comment_id)
    ''' Comment object for this view.
    '''

    if not request.user.is_staff and not request.user.is_superuser and \
    comment.author != request.user:
        return HttpResponseRedirect(
            reverse('index')
        )

    if request.method == "POST":
        ''' If this view is called using the POST method ...
        '''

        change_comment_form = ChangeCommentForm(
            request.POST, instance=comment, issue_status=comment.issue.status)
        ''' Get the data from the POST request but saving for this issue.
        '''

        if change_comment_form.is_valid():
            ''' If this form's data is valid then create the new Comment
            object.
            '''
            comment.issue.status = change_comment_form.cleaned_data['status']
            ''' Change the issue's status as needed.
            '''
            comment.issue.save()
            ''' Save the issue's status.
            '''
            comment.issue_status = comment.issue.status
            ''' Set the comment's issue status tracking.
            '''
            comment = change_comment_form.save()
            ''' Save data from this form to the same comment.
            '''

            return HttpResponseRedirect(reverse(
                'issue', kwargs={'issue_id': comment.issue.id}))
            ''' Send the user back to the issue's page.
            '''

    else:
        ''' If this view is called by any other method besides POST --
        usually 'GET' ...
        '''
        change_comment_form = ChangeCommentForm(
            instance=comment, issue_status=comment.issue.status)
        ''' Create a change comment form based on the comment instance.
        '''

    view_context = {
        'comment': comment,
        'change_comment_form': change_comment_form,
        'page_title': 'Issuetrack - Change Comment - {}'.format(comment.id),
    }
    ''' Context used for this view:
        comment:                Comment for this view.
        change_comment_form:    Our generated change_comment_form.
        page_title:             Title of the html page.
    '''

    view_context.update(TEMPLATE_CONTEXT)
    ''' Add standard template context from Issuetrack settings file.
    '''

    template_file = os.path.join(TEMPLATE_DIR, 'change_comment.html')
    ''' Template file used by this view.
    '''

    return render(request, template_file, view_context)


@login_required(login_url=LOGIN_URL)
def change_project(request, project_id):
    ''' View: /project/<project_id>/change/
    '''

    project = Project.objects.get(pk=project_id)

    if not request.user.is_staff and not request.user.is_superuser and \
    project.owner != request.user:
        return HttpResponseRedirect(
            reverse('project', kwargs={'project_id': project_id})
        )

    if request.method == "POST":
        ''' If this view is called using the POST method ...
        '''

        change_project_form = ChangeProjectForm(request.POST, instance=project)
        ''' Get the data from the POST request but saving for this issue.
        '''

        if change_project_form.is_valid():
            ''' If this is form's data is valid then create the new
            Project object.
            '''
            project = change_project_form.save()
            ''' Save data from this form to the same project.
            '''

            return HttpResponseRedirect(reverse(
                'project', kwargs={'project_id': project.id}))
            ''' Send the user back to the project page.
            '''

    else:
        ''' If this view is called by any other method besides POST --
        usually 'GET' ...
        '''
        change_project_form = ChangeProjectForm(instance=project)
        ''' Create a change project form based on the project instance.
        '''

    view_context = {
        'project': project,
        'change_project_form': change_project_form,
        'page_title': 'Issuetrack - Change Project - {}'.format(project.id),
    }
    ''' Context used for this view:
        project:                Project for this view.
        change_project_form:    Our generated change_project_form.
        page_title:             Title of the html page.
    '''

    view_context.update(TEMPLATE_CONTEXT)
    ''' Add standard template context from Issuetrack settings file.
    '''

    template_file = os.path.join(TEMPLATE_DIR, 'change_project.html')
    ''' Template file used by this view.
    '''

    return render(request, template_file, view_context)


@login_required(login_url=LOGIN_URL)
def change_component(request, component_id):
    ''' View: /component/<component_id>/change/
    '''

    component = Component.objects.get(pk=component_id)

    if not request.user.is_staff and not request.user.is_superuser and \
    component.project.owner != request.user:
        return HttpResponseRedirect(
            reverse('project', kwargs={'project_id': component.project.id})
        )

    if request.method == "POST":
        ''' If this view is called using the POST method ...
        '''

        change_component_form = ChangeComponentForm(
            request.POST, instance=component)
        ''' Get the data from the POST request but saving for this issue.
        '''

        if change_component_form.is_valid():
            ''' If this is form's data is valid then create the new
            Component object.
            '''
            component = change_component_form.save()
            ''' Save data from this form to the same component.
            '''

            return HttpResponseRedirect(reverse(
                'project', kwargs={'project_id': component.project.id}))
            ''' Send the user back to the project page.
            '''

    else:
        ''' If this view is called by any other method besides POST --
        usually 'GET' ...
        '''
        change_component_form = ChangeComponentForm(instance=component)
        ''' Create a change component form based on the component instance.
        '''

    view_context = {
        'component': component,
        'change_component_form': change_component_form,
        'page_title': 'Issuetrack - Change Component - {}'.format(
            component.name),
    }
    ''' Context used for this view:
        component:              Component for this view.
        change_component_form:  Our generated change_component_form.
        page_title:             Title of the html page.
    '''

    view_context.update(TEMPLATE_CONTEXT)
    ''' Add standard template context from Issuetrack settings file.
    '''

    template_file = os.path.join(TEMPLATE_DIR, 'change_component.html')
    ''' Template file used by this view.
    '''

    return render(request, template_file, view_context)


def delete_project(request, project_id):
    ''' View: /project/<project_id>/delete/
    '''

    project = Project.objects.get(pk=project_id)

    if not request.user.is_staff and not request.user.is_superuser and \
    project.owner != request.user:
        return HttpResponseRedirect(
            reverse('project', kwargs={'project_id': project_id})
        )

    project.delete()

    return HttpResponseRedirect(reverse('projects'))


def delete_component(request, component_id):
    ''' View: /component/<component_id>/delete/
    '''

    component = Component.objects.get(pk=component_id)

    if not request.user.is_staff and not request.user.is_superuser and \
    component.project.owner != request.user:
        return HttpResponseRedirect(
            reverse('project', kwargs={'project_id': project_id})
        )

    component.delete()

    return HttpResponseRedirect(
        reverse('project', kwargs={'project_id': component.project.id})
    )
