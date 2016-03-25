from django.forms import ModelForm
from issuetrack.models import Component, Issue, Project

class AddIssueForm(ModelForm):
	
	class Meta:
		
		model = Issue
		
		fields = [
			'title', 'description', 'kind', 
			'priority', 'urgency', 'component',
		]

class AddProjectForm(ModelForm):

	class Meta:

		model = Project

		fields = [
			'name', 'key', 'owner', 'description', 'members',
		]

class AddComponentForm(ModelForm):

	class Meta:

		model = Component

		fields = [
			'name', 'description',
		]