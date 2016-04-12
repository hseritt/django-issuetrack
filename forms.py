from django import forms
from django.forms import ModelForm
from issuetrack.models import Comment, Component, Issue, Project
from issuetrack.settings import ISSUE_STATUSES

class AddIssueForm(ModelForm):

	def __init__(self, *args, **kwargs):
		
		user = kwargs.pop('user')

		super(AddIssueForm, self).__init__(*args, **kwargs)
		
		if not user.is_staff or not user.is_superuser:
			''' Don't show assignee field unless user is staff user or superuser.
			'''
			del(self.fields['assignee'])
	
	class Meta:
		
		model = Issue
		
		fields = [
			'title', 'assignee', 'description', 'steps', 'observed', 
			'expected', 'kind', 'priority', 'urgency', 'component',
		]

	def clean(self):
		
		cleaned_data = super(AddIssueForm, self).clean()
		
		kind = cleaned_data.get('kind')
		steps = cleaned_data.get('steps')
		observed = cleaned_data.get('observed')
		expected = cleaned_data.get('expected')

		if kind == 'Bug' or kind == 'Improvement':
			
			if not steps or not observed or not expected:
				
				raise forms.ValidationError(
					"Steps to Replicate, Observed Behavior and Expected Behavior fields must be filled out if this issue is being created as a Bug or an Improvement."
				)


class ChangeIssueForm(ModelForm):

	class Meta:
		
		model = Issue
		
		fields = [
			'title', 'assignee', 'description', 'steps', 'observed', 
			'expected', 'kind', 'priority', 'urgency', 'component',
		]


class AddProjectForm(ModelForm):

	def __init__(self, *args, **kwargs):
		
		super(AddProjectForm, self).__init__(*args, **kwargs)
		
		self.fields['description'].widget.attrs.update(
			{
				'class': 'mceNoEditor',
			}
		)

	class Meta:

		model = Project

		fields = [
			'name', 'key', 'owner', 'description', 'members',
		]


class ChangeProjectForm(ModelForm):

	def __init__(self, *args, **kwargs):
		
		super(ChangeProjectForm, self).__init__(*args, **kwargs)
		
		self.fields['description'].widget.attrs.update(
			{
				'class': 'mceNoEditor',
			}
		)

	class Meta:

		model = Project

		fields = [
			'name', 'key', 'owner', 'description', 'members',
		]


class AddComponentForm(ModelForm):

	def __init__(self, *args, **kwargs):
		
		super(AddComponentForm, self).__init__(*args, **kwargs)
		
		self.fields['description'].widget.attrs.update(
			{
				'class': 'mceNoEditor',
			}
		)

	class Meta:

		model = Component

		fields = [
			'name', 'description',
		]
		

class ChangeComponentForm(ModelForm):

	def __init__(self, *args, **kwargs):
		
		super(ChangeComponentForm, self).__init__(*args, **kwargs)
		
		self.fields['description'].widget.attrs.update(
			{
				'class': 'mceNoEditor',
			}
		)

	class Meta:

		model = Component

		fields = [
			'name', 'description',
		]
		

class AddCommentForm(ModelForm):

	status = forms.ChoiceField(
		choices=ISSUE_STATUSES, 
		label='Set Status After Comment', 
	)

	def __init__(self, *args, **kwargs):
		
		try:
			self.issue_status = kwargs.pop('issue_status')
		except KeyError:
			pass

		super(AddCommentForm, self).__init__(*args, **kwargs)

		try:
			self.fields['status'].initial = self.issue_status
		except AttributeError:
			pass

	class Meta:

		model = Comment

		fields = [
			'status', 'text', 'audience',
		]


class ChangeCommentForm(AddCommentForm):

	def __init__(self, *args, **kwargs):
		
		try:
			self.issue_status = kwargs.pop('issue_status')
		except KeyError:
			pass

		super(ChangeCommentForm, self).__init__(*args, **kwargs)

		try:
			self.fields['status'].initial = self.issue_status
		except AttributeError:
			pass