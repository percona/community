---
id: "2ee674d0-91f3-80c2-90a1-d3b84f25732c"
title: "Implementando alta disponibilidade e continuidade de serviço no MySQL nos dias atuais"
layout: single
speakers:
  - fernando_laudares_camargos
talk_url: "https://mysqlbr.com.br/agenda/"
presentation_date: ""
presentation_date_end: ""
presentation_time: ""
talk_year: "2025"
event: "MySQL BR Conf 2025"
event_status: "Done"
event_date_start: "2025-10-04"
event_date_end: ""
event_url: ""
event_location: "São Paulo, Brazil"
talk_tags: ['MySQL']
slides: ""
video: ""
---
## Abstract

A 25 anos atrás, a introdução da replicação nativa contribuiu para fazer do MySQL o banco de dados mais utilizado pelas principais aplicações movendo a Internet. A essência do conceito permanece a mesma: se algo der errado com o servidor principal, os dados continuam disponíveis “online” na réplica. Mas a maneira como essa solução é implementada evoluiu bastante. Aliás, hoje contamos com mais de uma opção.
Recentemente, me encontrei trabalhando em três projetos muito similares envolvendo HA para MySQL e continuidade de serviço. Porém, os requisitos de cada um eram tais que me vi sugerindo uma implentação diferente em cada caso.
Nessa apresentação, uso as características desses projetos como pano de fundo para destacar as diferenças entre a replicação assíncrona traditional e a semi-síncrona, que hoje pode ser implementada tanto com o plugin Galera, utilizado pelo Percona XtraDB Cluster (PXC) e MariaDB Cluster, quanto pelo Group Replication, que constitui a base do InnoDB Cluster.