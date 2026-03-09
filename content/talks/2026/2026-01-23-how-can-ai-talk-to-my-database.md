---
id: 2ee674d0-91f3-8016-9c07-e1469f56bdf8
title: How Can AI Talk to My Database?
layout: single
speakers:
- fernando_laudares_camargos
talk_url: https://buildevcon.com/ai-dba-self-driving-databases/
presentation_date: '2026-01-23'
presentation_date_end: ''
presentation_time: ''
talk_year: '2026'
event: 'AI DBA: Self-Running Databases'
event_status: Accepted
event_date_start: '2026-01-23'
event_date_end: ''
event_url: https://buildevcon.com/ai-dba-self-driving-databases/
event_location: 'Virtual '
talk_tags:
- MySQL
- PostgreSQL
- ai
- Open Source
slides: ''
video: ''
images:
- talks/2026/2026-01-23-how-can-ai-talk-to-my-database.png
---
## Abstract

What if we want to give AI access to our database, so it is able to actually query it?

The most common way to provide an AI model access to different data sources (and tools!) is through the use of an intermediate server that implements the Model Context Protocol (MCP), which is an open standard. We call those intermediate MCP servers, and you can somewhat easily build one for different purposes. Having said that, chances are there's already an open source MCP server available out there that will cover your needs, including database access.

In this short presentation, I'll show how to use the FastMCP Python framework to deploy MCP servers that allow AI assistants like Claude and Gemini interact with MySQL and PostgreSQL databases.