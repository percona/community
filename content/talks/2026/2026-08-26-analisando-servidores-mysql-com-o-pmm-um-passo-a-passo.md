---
id: SPEAK-2232
jira: SPEAK-2232
title: 'Analisando servidores MySQL com o PMM: um passo a passo'
layout: single
speakers:
- fernando_laudares_camargos
talk_url: https://mysqlbrconf.com.br/schedule#s=analyzing-mysql-servers-pmm
presentation_date: '2026-08-26'
presentation_date_end: ''
presentation_time: '14:00'
talk_year: '2026'
event: MySQL Brazil Conference 2026
event_jira: SPEAK-1220
event_status: Done
event_date_start: '2026-09-26'
event_date_end: ''
event_url: https://mysqlbrconf.com.br/
event_location: Brazil - São Paulo
talk_tags:
- MySQL
slides: ''
video: ''
images:
- talks/2026/2026-08-26-analisando-servidores-mysql-com-o-pmm-um-passo-a-passo.png
---
Daqui a poucas semanas, o Percona Monitoring and Management (PMM) completará 10 anos (ou já completou, se considerarmos a primeira versão beta, lançada em abril de 2016). Como uma das primeiras soluções de monitoramento open source dedicadas ao MySQL, o PMM mudou a forma como nossa comunidade acompanha o que está acontecendo em seus servidores. Ao longo dos anos, o PMM foi expandido para oferecer suporte ao MongoDB, PostgreSQL e, mais recentemente, ao Valkey, mas tudo começou com o MySQL.  Nesta apresentação de 30 minutos, vou mostrar uma rotina prática para analisar um servidor MySQL com o PMM. Partindo dos dashboards gerais do MySQL e avançando até métricas específicas do InnoDB, vou demonstrar como correlacionar estes dados com métricas do sistema operacional para identificar gargalos de desempenho e utilizar o Query Analytics (QAN) para encontrar potenciais responsáveis por alguns dos problemas.  Seja para quem está conhecendo o PMM agora ou para quem já o utiliza para monitorar servidores MySQL, esta sessão ajudará você a navegar pelos dashboards de forma mais eficiente e a desenvolver uma abordagem prática para diagnosticar problemas de desempenho no MySQL.