{{ range $category, $list := .Site.Data.youtube }}
<h2>{{ $category }}</h2>
{{ range $list }}
<div class="youtubeList__container">
<div class="youtubeList__img">
    <a href="https://youtu.be/{{ .youtube_id }}" class="youtube__img" target="_blank"><img width="180px" src="https://img.youtube.com/vi/{{ .youtube_id }}/hqdefault.jpg" alt="" /></a>
</div>
<div class="youtubeList__text">
<p class="youtubeList__title"><a href="https://youtu.be/{{ .youtube_id }}" class="" target="_blank">{{ .title }}</a></p>
<p class="youtubeList__authors">{{ .authors }} - {{ .date }}</p>
</div>
</div>
{{end}}
{{end}}
<div class="json" style="display: none;">{{ .Site.Data.youtube | jsonify }}</div>
{{ .Inner }}
