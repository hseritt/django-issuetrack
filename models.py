''' Models used for the Issuetrack application.
'''

from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
	''' Project can be something like a software application or ongoing event or project.
	'''

	name = models.CharField('Name', max_length=30, unique=True)
	''' Name of the project.
	'''
	key = models.CharField('Key', max_length=10, unique=True)
	''' A unique 10 letter (or less) key for the project.
	'''
	owner = models.ForeignKey(User)
	''' A technical user who is the manager/owner or main stakeholder for the project.
	'''
	description = models.TextField('Description', null=True, blank=True)
	''' Describes the project.
	'''
	members = models.ManyToManyField(User, related_name='project_members')
	''' A list of users are eligible to be assignees or issue creaters for the project.
	'''

	def __str__(self):
		''' String repr of the Project is its name.
		'''
		return self.name


class Component(models.Model):
	''' A particular area of a project. For example a component for a software project could be 'models' or 'database' or 'UI'.
	'''

	name = models.CharField('Name', max_length=30)
	''' The component's name.
	'''
	project = models.ForeignKey(Project)
	''' Associated project.
	'''
	description = models.TextField('Description', null=True, blank=True)
	''' Optional description of the component.
	'''

	class Meta:
		''' Meta properties of the Component class go here.
		'''
		unique_together = (
			('name', 'project')
		)
		''' The name and project must be unique together.
		'''

	def __str__(self):
		''' String repr of the Component.
		'''
		return '{}/{}'.format(
			self.project.name,
			self.name
		)


class Issue(models.Model):

	title = models.CharField('Title', max_length=255)
	''' The issue's title.
	'''
	description = models.TextField('Description')
	''' A description of the issue.
	'''
	kind = models.CharField(
		'Kind', 
		max_length=30,
		choices=(
			('Bug', 'Bug'),
			('Improvement', 'Improvement'),
			('Feature', 'Feature'),
			('Info', 'Info'),
			('Proposal', 'Proposal'),
			('Task', 'Task'),
		)
	)
	''' The kind or type of issue.
	'''
	priority = models.CharField(
		'Priority',
		max_length=30,
		choices=(
			('Blocker', 'Blocker'),
			('Critical', 'Critical'),
			('Major', 'Major'),
			('Minor', 'Minor'),
			('Trivial', 'Trivial'),
		)
	)
	''' The priority for the issue.
	'''
	urgency = models.CharField(
		'Urgency',
		max_length=30,
		choices=(
			('ASAP', 'ASAP'),
			('7 days', '7 days'),
			('21 days', '21 days'),
			('42 days', '42 days'),
			('Indefinite', 'Indefinite'),
		)
	)
	''' The urgency for the issue. Sets an expectation of when an issue should be resolved.
	'''
	status = models.CharField(
		'Status',
		max_length=30,
		choices=(
			('New', 'New'),
			('Open', 'Open'),
			('In Progress', 'In Progress'),
			('Resolved', 'Resolved'),
			('Closed', 'Closed'),
			('On Hold', 'On Hold'),
			('Pending Creater', 'Pending Creater'),
			('Pending 3rd Party', 'Pending 3rd Party'),
			('Duplicate', 'Duplicate'),
			('Invalid/Unfounded', 'Invalid/Unfounded'),
			("Won't Fix", "Won't Fix"),
		),
		default='New',
	)
	''' The status or disposition of the issue.
	'''
	creater = models.ForeignKey(User)
	''' The user who created the issue.
	'''
	assignee = models.ForeignKey(
		User, null=True, blank=True, related_name='issue_assignee')
	''' The user who is assigned as the agent responsible for disposition of the issue.
	'''
	created = models.DateTimeField(auto_now_add=True)
	''' The date and time when the issue was created.
	'''
	modified = models.DateTimeField(auto_now=True)
	''' The date and time when the issue was last updated.
	'''
	component = models.ForeignKey(Component, null=True, blank=True)
	''' Associates with the Component.
	'''

	def __str__(self):
		''' String repr of the issue using the issue's title.
		'''
		return self.title


class Comment(models.Model):
	''' Associated comment for an issue.
	'''
	issue = models.ForeignKey(Issue)
	''' Associated issue the comment is for.
	'''
	text = models.TextField('Comment')
	''' The comment's text.
	'''
	author = models.ForeignKey(User)
	''' User who created the comment.
	'''
	created = models.DateTimeField(auto_now_add=True)
	''' The date and time when the comment was created.
	'''
	modified =  models.DateTimeField(auto_now=True)
	''' The date and time when the comment was last modified.
	'''
	audience = models.CharField(
		'Audience', 
		max_length=30,
		choices=(
			('Public', 'Public'),
			('Private', 'Private'),
		)
	)
	''' Who the comment is intended for.
	'''

	def __str__(self):
		''' String repr of the comment. Includes the issue title, comment author and the date and time when the comment was created.
		'''
		return 'Comment for "{}" by {} at {}'.format(
			self.issue.title, self.author, self.created
		)