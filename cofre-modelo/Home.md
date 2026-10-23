---
tipo: moc
titulo: "Home"
aliases: ["Home", "Início"]
escopo: "Porta de entrada do cofre de trabalho"
criado: 2026-10-23
atualizado: 2026-10-23
fonte_captura: manual
sigilo: ok
tags: [moc]
---

# Home

## Mapas
- Sistemas: crie uma nota `SIS-<slug>` em `20-Sistemas/` para cada sistema em que você trabalha.
- Banco de dados: depois de importar um dicionário (`_sistema/scripts/importar_dicionario.py`), ligue aqui o índice gerado em `22-Banco/`.
- Regras do cofre: `_sistema/REGRAS.md`.

## Como guardar algo
| Quero guardar | Como |
|---|---|
| Tentativa e erro / problema resolvido | Numa sessão do Claude: *"registra no cérebro o que aprendemos"*, ou nova nota com o modelo **licao** |
| Decisão | *"guarda essa decisão"*, ou o modelo **decisao** |
| Reunião | modelo **reuniao** |
| Conceito técnico, artigo | *"guarda no cérebro: …"*, ou os modelos **conceito** e **fonte** |
| Anotação rápida sem destino | nota diária ou nova nota em `00-Inbox/` |

## Lições em aberto
```base
filters:
  and:
    - 'note.tipo == "licao"'
    - '!file.inFolder("_sistema")'
views:
  - type: table
    name: Lições
    groupBy:
      property: note.situacao
      direction: DESC
    order: [file.name, note.titulo, note.sistema, note.data]
```

## Decisões recentes
```base
filters:
  and:
    - 'note.tipo == "decisao"'
    - '!file.inFolder("_sistema")'
views:
  - type: table
    name: Decisões
    order: [file.name, note.titulo, note.situacao, note.data]
```

## Inbox
```base
filters:
  and:
    - file.inFolder("00-Inbox")
views:
  - type: table
    name: A triar
    order: [file.name, file.ctime]
```
