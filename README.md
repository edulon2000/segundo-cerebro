# segundo-cerebro

Plugin do [Claude Code](https://docs.claude.com/claude-code) para manter um **segundo cérebro de trabalho no Obsidian**: lições aprendidas (tentativas e erros, causa raiz, solução), decisões, conceitos, reuniões e dicionário de dados, capturados direto das conversas com o Claude e ligados entre si.

Foi pensado para quem trabalha com dados sob **sigilo fiscal**. Nada de contribuinte entra nas notas, e as pastas com dados de trabalho ficam fora do alcance do Claude.

## O que vem no plugin

| Peça | O que faz |
|---|---|
| **Skill** `segundo-cerebro` | Na própria conversa: "guarda no cérebro: …", "registra o que aprendemos hoje", "o que já tentei sobre …". Faz a triagem, escolhe o tipo de nota, procura nota parecida, grava a partir do modelo e verifica sigilo. |
| **Agente** `segundo-cerebro` | Trabalho em lote: várias lições de uma vez, revisão da Inbox, juntar notas duplicadas, consultas amplas. Usa a skill. |
| **Hook** de bloqueio (G4) | Recusa qualquer leitura ou comando que cite `10-Demandas/`, `21-Componentes/` ou `_sistema/dados/`, em qualquer projeto. |
| **Verificador de sigilo** | Detecta e mascara CPF, CNPJ (numérico e alfanumérico), Inscrição Estadual (PB), razão social, número de processo e segredos. Nunca imprime o valor encontrado. |
| **Comando** `/segundo-cerebro:init` | Cria o cofre a partir do modelo e registra onde ele fica. |
| **Cofre-modelo** | Estrutura de pastas, `REGRAS.md`, 11 modelos de nota (lição, decisão, reunião, conceito…), `Home.md`, configuração do Obsidian e script de importação de dicionário de dados. |

## Requisitos

- Claude Code
- [Obsidian](https://obsidian.md) 1.9 ou mais recente (para o plugin principal **Bases**)
- Python 3.9 ou mais recente, acessível como `python` (usado pelo hook, pelo verificador e pelos scripts)

## Instalação

No Claude Code:

```
/plugin marketplace add https://github.com/edulon2000/segundo-cerebro.git
/plugin install segundo-cerebro@segundo-cerebro
```

Depois, crie ou complete o seu cofre:

```
/segundo-cerebro:init C:/Users/<voce>/Documents/Obsidian/MeuCofre
```

O `init` não sobrescreve nada que já exista na pasta. Ele grava o caminho do cofre em `~/.claude/segundo-cerebro.json`. Para usar outro cofre numa sessão, defina a variável `CEREBRO_COFRE`.

Para atualizar: `/plugin marketplace update segundo-cerebro` e reinicie o Claude Code.

## Uso

Em qualquer projeto, durante o trabalho:

- **"guarda no cérebro: o timeout da reindexação era o pool de conexões; aumentei para 50"**: vira uma lição ligada ao sistema.
- **"registra no cérebro o que aprendemos hoje"**: o Claude revisa a conversa, lista as lições e decisões, pede o seu ok e grava.
- **"o que já tentei sobre erro de pool de conexões?"**: busca nas lições, decisões e conceitos e responde com links.
- **"revisa a inbox do segundo cérebro"**: o agente promove, funde ou descarta cada item, registrando tudo no log.

Cada decisão de triagem (gravar, fundir, Inbox ou descartar) fica registrada em `_sistema/log/triagem-aaaa-mm.md`.

## Estrutura do cofre

```
00-Inbox/            dúvidas e anotações rápidas (revisão semanal)
10-Demandas/         uma nota por demanda (bloqueada para o Claude)
20-Sistemas/         SIS-<slug>
21-Componentes/      CMP-<sistema>-<Nome> (bloqueada para o Claude)
22-Banco/            dicionários de dados importados (gerado)
30-Reunioes/         REU-aaaa-mm-dd-<slug>
40-Decisoes/         DEC-aaaa-mm-dd-<slug>
50-Conhecimento/     Conceitos/ CON-, Fontes/ FON-, Licoes/ LIC-
60-Pessoas/          PES-<slug>
70-Projetos/         PRJ-<slug>
Diario/              aaaa-mm-dd
MOCs/                mapas de conteúdo
_sistema/            REGRAS.md, templates/, scripts/, log/, dados/ (bloqueada)
Home.md              porta de entrada
```

## Segurança

- **Regras:** veja as decisões-padrão em [`docs/decisoes-padrao.md`](docs/decisoes-padrao.md).
- **Duas camadas de bloqueio:** as regras `deny` em `.claude/settings.json` do cofre e o hook do plugin, que vale em todas as sessões.
- **Limite conhecido:** o hook vê o texto do comando, não o que ele lê. Um script que abra os arquivos sem citar a pasta passa.
- **Falha aberta:** sem Python, o hook deixa passar para não travar todas as sessões. As regras `deny` continuam valendo.
- **Antes de usar com dados de trabalho**, confirme a política da sua organização sobre IA e sobre onde o cofre pode ficar. O cofre-modelo desliga o Obsidian Sync.

Mais detalhes em [`docs/como-funciona.md`](docs/como-funciona.md).

## Testes

```
python -m unittest discover -s tests -v
```
