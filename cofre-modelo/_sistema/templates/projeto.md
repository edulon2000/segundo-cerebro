---
tipo: projeto
titulo: ""
aliases: []
status: ativo
objetivo: ""
demandas: []
sistemas: []
inicio: {{date:YYYY-MM-DD}}
prazo:
criado: {{date:YYYY-MM-DD}}
atualizado: {{date:YYYY-MM-DD}}
fonte_captura: manual
sigilo: ok
tags: [projeto]
---

# 

## Objetivo


## Situação atual


## Ligado a este projeto
```base
filters:
  and:
    - file.hasLink(this.file)
    - '!file.inFolder("_sistema")'
views:
  - type: table
    name: Ligadas a este projeto
    groupBy:
      property: note.tipo
      direction: ASC
    order: [file.name, note.titulo, note.status, note.situacao, note.atualizado]
```
