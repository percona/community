---
id: "2ee674d0-91f3-80e5-b65a-f5ef44b1558a"
title: "Projetando um sistema de check-in usando a \"nova\" replicação bidirecional"
layout: single
speakers:
  - fernando_laudares_camargos
talk_url: "https://2025.pgconf.com.br/talk?token=c508cb0d75fdc28448f68e21c249b84e"
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

Vamos nos preparar com antecedência; o turismo espacial está chegando!

Embora as passagens estarão certamente disponíveis online para aqueles com um limite de cartão de crédito alto o suficiente, não devemos ter a internet como garantida no espaço sideral. Quando o ônibus espacial parar em Marte para um passeio rápido, é melhor contarmos com um sistema que não dependa de um servidor hospedado na Terra para controlar o embarque e desembarque de passageiros. E se um alienígena decidir fazer o check-in no meio da viagem e uma supernova estiver bloqueando a conexão do satélite? Tenho certeza de que a indústria do turismo tem esse tipo de preocupação em mente ao planejar cruzeiros espaciais...

A ideia para este pequeno experimento (e apresentação) na verdade vem de um projeto de consultoria em que trabalhei com um aplicativo legado cujo processo de sincronização para dois servidores PostgreSQL independentes gerava alguns terabytes de arquivos temporários por dia para um banco de dados pequeno, com menos de 50 GB — mesmo quando não havia alterações no conjunto de dados, uma verdadeira abordagem de "força bruta"! Hoje em dia, existem maneiras melhores de conseguir isso, como usar a nova replicação bidirecional do PostgreSQL, que estreou na versão 16. Na realidade, esse não é um recurso novo, mas uma melhoria no código da replicação lógica que torna a replicação bidirecional possível. Aposto que você teria dificuldade em encontrar um "use case" melhor para isso do que turismo espacial!

Embora esta apresentação se concentre nessa funcionalidade estendida de replicação do PostgreSQL, ela começa discutindo schema design e o papel da definição da "fonte da verdade" para seus vários componentes, algo que muitas vezes é negligenciado no desenvolvimento de uma nova aplicação.