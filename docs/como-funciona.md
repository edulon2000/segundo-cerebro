# Como funciona

## Skill × agente

| | Skill | Agente |
|---|---|---|
| Onde roda | Dentro da conversa em curso | Em contexto próprio, separado |
| Vê o que foi tentado na sessão? | Sim | **Não**: recebe tudo por escrito no prompt |
| Melhor para | Uma captura rápida; registrar as lições da sessão | Lotes, revisão da Inbox, consolidação, consultas amplas |

Fluxo típico para "registra o que aprendemos hoje":

1. A conversa principal, que viu as tentativas, monta a lista e pede o seu ok.
2. Com poucos itens, ela mesma grava pela skill. Com muitos, delega ao agente, passando cada item completo e a frase "lista aprovada pelo usuário".
3. Sem essa frase, o agente só devolve a proposta e não grava nada.

## Triagem

Pergunta-guia: *vou reutilizar isso, decidir algo com base nisso ou explicar isso para alguém?*

| Destino | Quando |
|---|---|
| ARMAZENAR | Sim, e não existe nota sobre o assunto |
| FUNDIR | Já existe nota: acrescenta nela, sem reescrever o que está lá |
| INBOX | Dúvida; revisão semanal decide |
| DESCARTAR | Transitório, genérico ou fora do contexto; só o motivo vai para o log |

## Nota de lição (`LIC-`)

```
Problema · Contexto · Tentativas (o que tentei | resultado | por que não resolveu) · Causa raiz · Solução · Como evitar / reconhecer
```

`situacao`: `resolvida`, `contornada` (resolveu sem atacar a causa) ou `em_aberto`.

## Verificador de sigilo

`skills/segundo-cerebro/verificar_sigilo.py`:

| Detecta | Como |
|---|---|
| CPF | formatado sempre; sem formatação só com dígito verificador válido |
| CNPJ numérico e alfanumérico | idem (DV conforme a NT conjunta COCAD/SUARA/RFB nº 49/2024) |
| Inscrição Estadual | formato da PB (9 dígitos começando por 16), com DV |
| Razão social | heurística: palavras em maiúscula terminando em LTDA, S/A, EIRELI, EPP, MEI |
| Número de processo | numeração única do CNJ, ou "processo nº …" |
| Segredos | `senha=`, `token:`, `api_key=`, `Bearer …`, strings JDBC com senha, chaves privadas |

- Com `--mascarar`, substitui no próprio arquivo. Rodar de novo sobre a saída não acusa nada: o mascaramento é idempotente.
- **Não detecta** nome de pessoa física. Isso fica por conta da regra G1 na hora de redigir.

## Hook de bloqueio

`hooks/bloquear_leitura_sigilo.py` roda antes de Read, Edit, Write, Grep, Glob, Bash e PowerShell. Ele nega quando o caminho, ou o texto do comando, cita uma das pastas protegidas. Aceita `/` ou `\` e ignora maiúsculas e minúsculas.

Efeito colateral: comandos que só **mencionam** o nome dessas pastas também são negados. Para testar ou automatizar, coloque o caminho num arquivo ou script.

## Dicionário de dados

`_sistema/scripts/importar_dicionario.py` importa dicionários em Markdown (uma nota por tabela, FKs como wikilinks) para `22-Banco/<schema>/`:

- renomeia índices homônimos com o prefixo do schema e reescreve os links;
- só grava o que mudou e avisa quando a origem tem caracteres corrompidos (U+FFFD).

As origens ficam em `_sistema/config.json` (veja `config.exemplo.json`).

## Instalação manual, sem marketplace

Copie `skills/segundo-cerebro/` para `~/.claude/skills/` e `agents/segundo-cerebro.md` para `~/.claude/agents/`. Registre o hook em `~/.claude/settings.json` apontando para o caminho absoluto do script, e rode `scripts/init_cofre.py --destino <pasta>`.
