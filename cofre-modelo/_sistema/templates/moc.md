---
tipo: moc
titulo: ""
aliases: []
escopo: ""
criado: {{date:YYYY-MM-DD}}
atualizado: {{date:YYYY-MM-DD}}
fonte_captura: manual
sigilo: ok
tags: [moc]
---

# 

Para que serve este mapa e por onde começar.

## Principais
- 

## Ligado a este mapa
```base
filters:
  and:
    - file.hasLink(this.file)
    - '!file.inFolder("_sistema")'
views:
  - type: table
    name: Notas
    groupBy:
      property: note.tipo
      direction: ASC
    order: [file.name, note.titulo, note.atualizado]
```
