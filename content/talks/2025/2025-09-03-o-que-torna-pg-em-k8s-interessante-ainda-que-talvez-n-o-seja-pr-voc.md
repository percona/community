---
id: "2ee674d0-91f3-80ec-94a6-c9fa3278b757"
title: "O que torna PG em K8s interessante, ainda que (talvez) não seja prá você?"
layout: single
speakers:
  - fernando_laudares_camargos
talk_url: "https://2025.pgconf.com.br/talk?token=c7c14626bf7ea4976752c4c24bab4e2f"
presentation_date: "2025-09-03"
presentation_date_end: ""
presentation_time: ""
talk_year: "2025"
event: "PGConf.Brasil 2025"
event_status: "Done"
event_date_start: "2025-09-03"
event_date_end: "2025-09-05"
event_url: "https://2025.pgconf.com.br/"
event_location: "Brazil"
talk_tags: ['PostgreSQL']
slides: ""
video: ""
---
## Abstract

Como instalar um ambiente PostgreSQL em K8s utilizando o Percona Operator e quais são os principais atrativo e os maiores desafios dessa escolha.


"Nada", você pode estar pensando. Ao menos era o que eu pensava: "Kubernetes pode ser bom para rodar servidores de aplicação com uma certa 'elasticidade', mas não pode ser uma boa opção para bancos de dados, que devem rodar de forma estável e sem falhas". Contudo, embora os ambientes Kubernetes continuem sendo bastante "dinâmicos", eles evoluíram para melhor suportar aplicações do tipo "stateful", como bancos de dados, e a tecnologia agora conta com uma comunidade engajada em fazer avançar essa área, chamada de Data on Kubernetes (DoK), que segue crescendo. Por que será? Assim como Database-as-a-Service (DBaaS), a facilidade de implantação e gestão pode ser uma característica bastante atrativa do Kubernetes - isto é, quando utilizamos um operator para realizar o trabalho!

Nesta apresentação, explico como instalar um ambiente PostgreSQL em Kubernetes utilizando o Percona Operator for PostgreSQL que inclúi algumas das ferramentas e utilidades favoritas da comunidade: Patroni para alta disponibilidade, pgBackRest para backups e WAL archiving e pgBouncer para connection pooling. Adiciono o PMM para monitoramento e executo alguns workloads com o Sysbench para demonstrar o novo ambiente em funcionamento.

Pode parecer um how-to disfarçado de discussão sobre o assunto, e de certa maneira não deixa de ser: ainda que você não tenha familiaridade com o Kubernetes e esta seja a sua primeira experiência com ele, vou te mostrar como "subir" um novo ambiente no cloud com uma meia dúzia de comandos (nove, pare ser mais preciso). Portanto, meu objetivo principal é usar este ambiente para apresentar o que eu acho atrativo em rodar o PostgreSQL no Kubernetes e apontar os maiores desafios que eu vejo nessa empreitada. Daí você pode ter certeza que esse conjunto não é uma boa prá você; ou talvez seja?