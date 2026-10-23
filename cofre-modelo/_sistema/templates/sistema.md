---
tipo: sistema
titulo: ""
aliases: []
sigla: ""
stack: []
repositorios: []
categorias_redmine: []
schemas: []
responsaveis: []
criado: {{date:YYYY-MM-DD}}
atualizado: {{date:YYYY-MM-DD}}
fonte_captura: manual
sigilo: ok
tags: [sistema]
---

# 

## Visão geral


## Integrações
- 

## Ligado a este sistema
```base
filters:
  and:
    - file.hasLink(this.file)
    - '!file.inFolder("_sistema")'
views:
  - type: table
    name: Demandas abertas
    filters:
      and:
        - 'note.tipo == "demanda"'
        - 'note.status != "fechada"'
        - 'note.status != "rejeitada"'
    order: [file.name, note.titulo, note.status, note.prazo]
  - type: table
    name: Lições
    filters:
      and:
        - 'note.tipo == "licao"'
    order: [file.name, note.titulo, note.situacao, note.data]
  - type: table
    name: Decisões e componentes
    filters:
      or:
        - 'note.tipo == "decisao"'
        - 'note.tipo == "componente"'
    groupBy:
      property: note.tipo
      direction: ASC
    order: [file.name, note.titulo, note.data]
```
