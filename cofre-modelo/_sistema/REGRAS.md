# REGRAS do cofre

> É o que a skill e o agente `segundo-cerebro` leem antes de agir. Ajuste à sua realidade.
> As decisões por trás das regras G1–G5 estão em `docs/decisoes-padrao.md` do repositório do plugin.

## 1. Restrições (vêm antes de tudo)

| # | Regra |
|---|---|
| G1 | Nenhum dado de contribuinte vai para o cofre nem para LLM: CPF, CNPJ (numérico ou alfanumérico), Inscrição Estadual, razão social, nome de pessoa física contribuinte, valores de operação ligados a um contribuinte. Mascarar antes de escrever. |
| G4 | O Claude **não lê nem altera** `10-Demandas/`, `21-Componentes/` e `_sistema/dados/`. Pode **linkar** para notas dessas pastas pelo ID (`[[RM-1234]]`, `[[CMP-sistema-Classe]]`) sem abri-las. |
| G5 | Número de processo vira `proc. ***`. |
| — | Nunca: credenciais, tokens, senhas, strings de conexão, stack trace inteiro (guarde só a causa raiz). |

## 2. Pastas e nomes

| Tipo | Pasta | Nome do arquivo | Quem escreve |
|---|---|---|---|
| `demanda` | `10-Demandas/` | `RM-<id>` | integração com o gerenciador de demandas (futuro) |
| `sistema` | `20-Sistemas/` | `SIS-<slug>` | você / skill |
| `componente` | `21-Componentes/<sistema>/` | `CMP-<sistema>-<NomeOriginal>` | integração / você |
| `tabela_bd`, `dicionario` | `22-Banco/<schema>/` | nome da tabela / `BD-<schema> — …` | `_sistema/scripts/importar_dicionario.py` (não editar) |
| `reuniao` | `30-Reunioes/` | `REU-<aaaa-mm-dd>-<slug>` | você / skill |
| `decisao` | `40-Decisoes/` | `DEC-<aaaa-mm-dd>-<slug>` | você / skill |
| `conceito` | `50-Conhecimento/Conceitos/` | `CON-<slug>` | você / skill |
| `fonte` | `50-Conhecimento/Fontes/` | `FON-<slug>` | você / skill |
| `licao` | `50-Conhecimento/Licoes/` | `LIC-<aaaa-mm-dd>-<slug>` | você / skill |
| `pessoa` | `60-Pessoas/` | `PES-<slug>` | você / skill |
| `projeto` | `70-Projetos/` | `PRJ-<slug>` | você / skill |
| `diario` | `Diario/` | `<aaaa-mm-dd>` | você / skill |
| `moc` | `MOCs/` | `MOC-<tema>` | você / skill |
| (dúvida) | `00-Inbox/` | livre | qualquer um |

- **Slug:** minúsculas, sem acento, palavras separadas por hífen (`gestao-de-documentos`). Componentes e tabelas mantêm o nome original do código ou do banco.
- **O nome do arquivo é o ID.** O título legível vai em `titulo`, `aliases` e no H1. Não use `#` no nome do arquivo, porque ele quebra os wikilinks.
- **Links sempre por ID**, com alias de exibição: `[[RM-1234|Ajuste no cálculo]]`, `[[SIS-meu-sistema|Meu Sistema]]`.
- Sistemas deste cofre: *(liste aqui os seus, ex.: `SIS-meu-sistema`)*.

## 3. Propriedades comuns (todas as notas)

```yaml
tipo:            # da tabela acima
titulo: ""
aliases: []
criado: aaaa-mm-dd
atualizado: aaaa-mm-dd
fonte_captura:   # manual | conversa | web | reuniao | redmine | git
sigilo: ok       # ok | revisar | bloqueado
tags: []
```

As propriedades específicas de cada tipo estão nos modelos de `_sistema/templates/`. **Toda nota nasce de um modelo.**

## 4. Triagem

**Pergunta-guia:** *vou reutilizar isso, decidir algo com base nisso ou explicar isso para alguém?*

| Destino | Quando |
|---|---|
| ARMAZENAR | Sim à pergunta-guia e não existe nota sobre o assunto |
| FUNDIR | Já existe nota sobre o mesmo assunto, sistema ou componente: acrescentar nela |
| INBOX | Dúvida |
| DESCARTAR | Transitório, genérico (achável no Google) ou sem relação com o meu contexto |

Sempre ARMAZENAR ou FUNDIR: decisão explícita, problema com causa raiz encontrada (vira `licao`), pedido explícito, `#guardar`.

**Revisão semanal da Inbox:** cada item é promovido, fundido ou descartado. Item parado há mais de 14 dias é descartado, com registro no log.

Toda decisão de triagem vira uma linha em `_sistema/log/triagem-aaaa-mm.md`:

```
| data | fonte | resumo (1 linha) | destino | motivo | nota |
```

## 5. Escrita

- **Antes de criar, procurar:** busca por título, alias e palavras-chave em `20-Sistemas`, `30-Reunioes`, `40-Decisoes`, `50-Conhecimento`, `60-Pessoas`, `70-Projetos`, `MOCs` e `00-Inbox`. Nunca nas pastas da G4.
- **Nada órfão:** toda nota liga a pelo menos um sistema, projeto, demanda ou MOC.
- **Texto humano é intocável.** Ao fundir, acrescente; não reescreva o que já está lá. Só o código reescreve o que está entre `<!-- auto:… -->`.
- `atualizado` só muda quando o conteúdo muda.
- Depois de escrever, rodar o verificador de sigilo sobre o arquivo.
