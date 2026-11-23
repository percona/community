---
name: {{ .Name }}
name_pronunciation: {{ replace .Name "_" " " | title }}
fullname: {{ replace .Name "_" " " | title }}
fullname_pronounciation: {{ replace .Name "_" " " | title }}
# Percona staff: "Role @ Percona". Community: role and company, or leave empty.
job: 
tagline: 
social:
  website: 
  facebook: 
  twitter: 
  github: 
  linkedin: 
images:
- contributors/{{ .Name }}.jpg
# Badge next to the name: current (Percona staff), former (ex-Percona), community.
status: community
# Staff / Community filter on /contributors/: staff (current or former Percona), community.
contributor_status:
- community
# Auto-generated fields. Do not edit manually.
contributor_type: []
contributor_tag: []
events_tags: []
blog_tags: []
posts_count: 0
talks_count: 0
---
Enter the full bio text here.
