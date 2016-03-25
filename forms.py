from django.forms import ModelForm
from issuetrack.models import Issue

class AddIssueForm(ModelForm):
	
	class Meta:
		
		model = Issue
		
		fields = [
			'title', 'description', 'kind', 
			'priority', 'urgency', 'component',
		]