---
# This is the title of the post.
title: "{{ replace .Name "-" " " | title }}"
# This is the publish date. If this is in the future it will not be shown.
date: "{{ .Date }}"
images:
  # Add social images as a list here. The images must be referenced relative
  # to the assets directory. The image will be resized to be 1200 pixels
  # wide. If a single image is provided some sites will take the middle
  # 1200x630 pixels, while others will take the full image.
  #
  # e.g.:
  # - post-tag/social.png
authors:
  # Add a list of authors here. The names must be authors that exist in the
  # authors section. Their bio will be pulled from their author page.
  # E.g.:
  # - sanja
---

** Insert lead paragraph here **