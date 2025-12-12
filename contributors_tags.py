#!/usr/bin/env python3
import os
import frontmatter
from collections import defaultdict

BLOG_DIR = "content/blog"
EVENTS_DIR = "content/events"
CONTRIB_DIR = "content/contributors"

author_categories = defaultdict(set)
author_posts_count = defaultdict(int)
author_talks_count = defaultdict(int)
author_types = defaultdict(set)

# Step 1: collect categories from blog posts
for root, _, files in os.walk(BLOG_DIR):
    for f in files:
        if f.endswith(".md"):
            post = frontmatter.load(os.path.join(root, f))
            categories = post.get("categories", [])
            authors = post.get("authors", [])
            for a in authors:
                author_categories[a].update(categories)
                author_posts_count[a] += 1
                author_types[a].add("blog")

# Step 2: collect talks from events
for root, _, files in os.walk(EVENTS_DIR):
    for f in files:
        if f.endswith(".md"):
            event = frontmatter.load(os.path.join(root, f))
            speakers = event.get("speakers", [])
            for s in speakers:
                author_talks_count[s] += 1
                author_types[s].add("talks")

# Step 3: update contributors
for root, _, files in os.walk(CONTRIB_DIR):
    for f in files:
        if f.endswith(".md"):
            path = os.path.join(root, f)
            contrib = frontmatter.load(path)
            name = contrib.get("name")

            if name:
                # Merge categories into tags
                existing_tags = set(contrib.get("tags", []))
                new_tags = author_categories[name]
                merged_tags = sorted(existing_tags.union(new_tags))
                if merged_tags:
                    contrib["tags"] = merged_tags

                # Update counts
                if author_posts_count[name] > 0:
                    contrib["posts_count"] = author_posts_count[name]
                if author_talks_count[name] > 0:
                    contrib["talks_count"] = author_talks_count[name]

                # Update type
                if author_types[name]:
                    contrib["type"] = sorted(author_types[name])

                # Write back
                with open(path, "w") as out:
                    frontmatter.dump(contrib, out)
                print(f"Updated {path}: tags={merged_tags}, posts={author_posts_count[name]}, talks={author_talks_count[name]}, type={contrib.get('type')}")
