---
id: SPEAK-1461
jira: SPEAK-1461
title: Kubernetes desde la perspectiva de la base de datos
layout: single
speakers:
- edith_puclla
talk_url: https://ocgroups.dev/cncf/group/e5vgp72/event/qhtdje9
presentation_date: '2026-06-10'
presentation_date_end: ''
presentation_time: 01:00
talk_year: '2026'
event: Cloud Native Mexico City
event_jira: SPEAK-1460
event_status: Done
event_date_start: '2026-06-09'
event_date_end: ''
event_url: https://ocgroups.dev/cncf/group/e5vgp72/event/qhtdje9
event_location: Mexico
talk_tags:
- CloudNative
- Kubernetes
- Cloud-Native
- Slides
slides: https://docs.google.com/presentation/d/1bjABAlOjasOiicSMn-j7lucCX2vMObYs6sZAUxXbIRo/edit?usp=sharing
video: ''
images:
- talks/2026/2026-06-10-kubernetes-desde-la-perspectiva-de-la-base-de-datos.png
---
En esta charla vamos a ver Kubernetes desde una perspectiva diferente: empezando por la base de datos. Usaremos un clúster PostgreSQL de tres nodos ejecutándose en Google Kubernetes Engine y desplegado con el Kubernetes Operator para PostgreSQL.La idea es comenzar desde psql, observando lo que ve una persona que trabaja con la base de datos, y luego conectar eso con lo que ocurre detrás en Kubernetes usando kubectl. Así podremos entender cómo Kubernetes, junto con un Operator, ayuda a gestionar tareas como despliegues, escalado, backups, usuarios, certificados y alta disponibilidad.En lugar de instalar y configurar PostgreSQL, la replicación o pgBouncer manualmente, veremos cómo podemos describir lo que queremos en un archivo y dejar que el Operator se encargue del resto. Usaremos herramientas completamente open source.