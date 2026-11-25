> For the complete site map for agents, see [llms.txt]({{ "llms.txt" | absURL }}).

# {{ .Site.Title }}

{{ with .Site.Params.description }}{{ . }}

{{ end -}}
Community site for people who run databases in production: events, talks, blog posts, speakers, and how to contribute. Not product docs — those live at https://docs.percona.com/.

Source: {{ .Permalink }}

## Agent entry points

- Site map: {{ "llms.txt" | absURL }}
- Full snapshot: {{ "llms-full.txt" | absURL }}
- Agent skill: {{ "skill.md" | absURL }}
- Search API docs: {{ "developers/" | absURL }}
- OpenAPI: {{ "openapi.json" | absURL }}
- AI Catalog: {{ ".well-known/ai-catalog.json" | absURL }}

{{ .RawContent }}
