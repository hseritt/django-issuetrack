# Django-Issuetrack

Should mimic in functionality that of the issue tracker used for GitHub and Bitbucket repositories.

## Objectives:

Plan to use the following models:

### Project
- Name
- Owner
- Members

### Issue
- Title
- Description
- Kind: bug, feature, enhancement, proposal, task, info
- Author that relates to 'user'.
- Created and modified dates
- Related components
- File attachment
- Priority: blocker, critical, major, minor, trivial
- Urgency: Urgent/important, Urgent/not important, Not urgent/important, Not urgent/not important
- Status: New, Open, In Progress, Resolved, Closed, On-hold, Pending Creater, Pending 3rd Party, Duplicate, Invalid/Unfounded, Won't Fix

### Comment
- Relate to Issue
