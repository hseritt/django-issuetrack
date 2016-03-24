from django.contrib import admin
from issuetrack.models import Comment, Component, Issue, Project

admin.site.register(Component)
admin.site.register(Issue)
admin.site.register(Project)
admin.site.register(Comment)