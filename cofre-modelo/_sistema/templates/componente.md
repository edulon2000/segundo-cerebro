---
tipo: componente
titulo: ""
aliases: []
categoria: classe
sistema: ""
caminho: ""
schema: ""
dicionario: ""
origem: manual
criado: {{date:YYYY-MM-DD}}
atualizado: {{date:YYYY-MM-DD}}
fonte_captura: manual
sigilo: ok
tags: [componente]
---

# 

## O que faz


## Armadilhas conhecidas
- 

## Ligado a este componente
```base
filters:
  and:
    - file.hasLink(this.file)
    - '!file.inFolder("_sistema")'
views:
  - type: table
    name: Demandas e lições
    groupBy:
      property: note.tipo
      direction: ASC
    order: [file.name, note.titulo, note.status, note.situacao]
```
