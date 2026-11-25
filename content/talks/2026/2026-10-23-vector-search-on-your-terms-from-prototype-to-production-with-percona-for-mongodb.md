---
id: SPEAK-3393
jira: SPEAK-3393
sync: skip
title: 'Vector Search on Your Terms: From Prototype to Production with Percona for
  MongoDB'
layout: single
speakers:
- radoslaw_szulgo
- sandra_romanchenko
talk_url: https://buildevcon.com/events/vector-in-databases
presentation_date: '2026-10-23'
presentation_date_end: ''
presentation_time: '14:01'
room: ''
talk_year: '2026'
event: Vector in Databases
event_jira: SPEAK-2671
event_status: Done
event_date_start: '2026-10-23'
event_date_end: '2026-10-23'
event_url: https://buildevcon.com/events/vector-in-databases
event_location: ''
talk_tags:
- ai
- databases
- vector-database
- Video
slides: ''
video: https://www.youtube.com/watch?v=Wjymxm6JQEs
youtube_id: Wjymxm6JQEs
images:
- talks/2026/2026-10-23-vector-search-on-your-terms-from-prototype-to-production-with-percona-for-mongodb.png
---
Vector search in MongoDB Community Edition is easy to turn on if you send your documents to a cloud API to build the embeddings. At Vector in Databases on October 23, Radoslaw Szulgo and Sandra Romanchenko showed what that costs you, and what you can do on Percona Server for MongoDB (PSMDB) instead.

Keyword search and full-text search still have a job. They miss the query that describes what you want without using the words stored in the document. Vector search covers that gap, and retrieval-augmented generation needs it when the answer has to come from your data. The hard part is not the distance math. It is keeping an embedding next to every insert and update.

Automatic embeddings in MongoDB Community Edition, as they described them, use a short list of Voyage AI models and send the document out to get the vector back. That breaks when the model you want is not on the list, or when the document cannot leave your network. Percona Search for MongoDB, on Percona Server for MongoDB 8.0 and later, can call any OpenAI-compatible endpoint: a local server such as Ollama or vLLM, or a hosted API. On October 23 this was a technical preview. They said general availability was set for October 28. You can also point it at the Hugging Face Inference API if you do not want to host the model.

Sandra showed a three-node replica set. Your application still issues insert, update, and delete. Percona Search for MongoDB reads the change stream, asks the model for a vector, and stores it beside the data, not in the same collection. A search comes back as ids and scores. The database loads the documents. A missing or degraded index does not raise an error. You get an empty result set, which is why the service and the index lifecycle sit on a Percona Monitoring and Management (PMM) dashboard.

The recording includes the board-game demo: a typo that full-text search catches, and a phrase that only vector search matches.

[Recording](https://www.youtube.com/watch?v=Wjymxm6JQEs)