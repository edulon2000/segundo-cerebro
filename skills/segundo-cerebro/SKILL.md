---
name: segundo-cerebro
description: Guarda e consulta conhecimento no segundo cérebro de trabalho do usuário (cofre Obsidian). Use quando o usuário disser "guarda no cérebro", "registra no cérebro", "anota isso", "registra o que aprendemos hoje", "guarda essa decisão", "isso é importante", "#guardar", ou perguntar "o que já tentei sobre…", "o que sei sobre…", "já resolvemos isso antes?", "o que o cérebro tem sobre…". Cobre lições (tentativas e erros, causa raiz, solução), decisões, conceitos técnicos, reuniões, fontes e pessoas. Funciona em qualquer projeto.
---

# Segundo cérebro

Arquivos de apoio, no diretório base desta skill (informado quando ela é carregada):
- `cofre.py`: informa onde está o cofre.
- `verificar_sigilo.py`: procura e mascara dados sob sigilo.

## 0. Antes de qualquer coisa

1. **Descubra o cofre:** `python "<diretório base desta skill>/cofre.py"`. Abaixo, `COFRE` é o caminho que ele imprimir. Se ele disser que não há cofre configurado, diga ao usuário para rodar `/segundo-cerebro:init <pasta>` e pare.
2. Leia `COFRE/_sistema/REGRAS.md`. Ele é a fonte da verdade e prevalece sobre este arquivo.
3. **Nunca leia, liste, busque nem edite** `COFRE/10-Demandas/`, `COFRE/21-Componentes/` ou `COFRE/_sistema/dados/` (regra G4). Pode escrever links para notas dessas pastas pelo ID (`[[RM-1234]]`, `[[CMP-sistema-Classe]]`) sem abri-las. Toda busca no cofre deve usar um caminho que exclua essas pastas.
4. **Nenhum dado de contribuinte** entra no cofre (G1): CPF, CNPJ, IE, razão social, nome de contribuinte, valor ligado a contribuinte, número de processo (G5). Ao redigir, substitua por `CPF ***`, `CNPJ ***`, `IE ***`, `[contribuinte]`, `proc. ***`. Também não entram senha, token, string de conexão nem stack trace inteiro: guarde só a causa raiz, em uma ou duas linhas.
5. Se o pedido depender de ler conteúdo de demanda, diga que pela G4 você não lê `10-Demandas/` e peça ao usuário o trecho necessário, já sem dado de contribuinte.

## 1. Escolher o que fazer

| Pedido | Fluxo |
|---|---|
| "guarda no cérebro: …", "anota isso", "#guardar" | **Capturar** (§2) |
| "registra o que aprendemos hoje", "guarda essa sessão", "anota as tentativas" | **Lição da sessão** (§3) |
| "o que já tentei sobre…", "o que sei sobre…", "já resolvemos isso?" | **Consultar** (§4) |

## 2. Capturar

1. **Triar** com a pergunta-guia: *vou reutilizar isso, decidir algo com base nisso ou explicar isso para alguém?*
   - Não: DESCARTAR. Diga isso ao usuário em uma linha e registre no log (§5).
   - Dúvida: INBOX. Crie uma nota curta em `COFRE/00-Inbox/`, com nome livre e descritivo.
   - Sim: siga para o passo 2.
2. **Classificar o tipo:** `licao` (havia um problema, com causa raiz ou tentativas), `decisao` (escolha entre alternativas), `conceito` (ideia técnica reutilizável), `reuniao`, `fonte` (artigo, doc, curso), `pessoa`, `projeto`, `sistema`.
3. **Procurar nota existente** antes de criar. Use Grep com `-i` pelo assunto, nomes de classe ou tabela e palavras-chave, **em todas estas pastas e só nelas**: `20-Sistemas`, `30-Reunioes`, `40-Decisoes`, `50-Conhecimento`, `60-Pessoas`, `70-Projetos`, `MOCs`, `00-Inbox`. Se encontrar nota sobre o mesmo assunto, FUNDIR: acrescente (nova linha em Tentativas, nova seção datada), nunca reescreva o que já estava lá, e atualize `atualizado`.
4. **Criar** a partir de `COFRE/_sistema/templates/<tipo>.md`:
   - Troque `{{date:YYYY-MM-DD}}` pela data de hoje e preencha `titulo`, `aliases` e o H1 com o título legível.
   - Use o nome de arquivo e a pasta de `REGRAS.md` §2. Exemplo: `50-Conhecimento/Licoes/LIC-2026-10-22-timeout-na-reindexacao.md`.
   - Use `fonte_captura: conversa` quando o conteúdo vier da sessão.
   - **Ligue** a nota a um sistema (`[[SIS-<slug>]]`), aos componentes (`[[CMP-<sistema>-<Nome>]]` ou a tabela do dicionário de dados) e à demanda (`[[RM-<id>]]`), quando o usuário citar. Nada fica órfão: no mínimo um sistema, projeto ou MOC.
   - Não crie nota de sistema, componente ou demanda só para o link resolver. Link pendente é aceitável.
5. **Verificar sigilo:** `python "<diretório base desta skill>/verificar_sigilo.py" --mascarar "<arquivo>"`. Se ainda houver achados, corrija à mão e rode de novo.
6. **Registrar** (§5) e **responder** (§6).

## 3. Lição da sessão

1. Releia a conversa atual e identifique cada problema distinto que teve causa encontrada ou que ainda está em aberto.
2. Para cada problema, crie uma nota `licao` com:
   - **Problema:** o sintoma, em uma ou duas linhas.
   - **Contexto:** sistema, ambiente, componente, demanda.
   - **Tentativas:** uma linha da tabela por tentativa real da sessão, incluindo as que falharam e por quê. É a parte mais valiosa.
   - **Causa raiz**, **Solução** e **Como evitar / reconhecer de novo**.
   - `situacao`: `resolvida`, `contornada` (resolveu sem atacar a causa) ou `em_aberto`.
3. Decisões tomadas na sessão viram notas `decisao` à parte, ligadas à lição.
4. Antes de criar, procure lições parecidas (§2.3) e funda quando for o mesmo problema.
5. Mostre ao usuário a lista do que vai gravar (título e tipo) **antes** de gravar, e grave depois do ok.
   - Se você é o **agente** `segundo-cerebro`, não há usuário para perguntar. Grave só se o prompt disser que a lista já foi aprovada; caso contrário, devolva a lista proposta.

## 4. Consultar

1. Busque (Grep `-i`) nas pastas permitidas de §2.3 e em `22-Banco/` (dicionário de dados), se existir.
2. Leia as notas encontradas e responda citando-as como links clicáveis.
3. Diga quando a resposta pode estar em demandas (`10-Demandas/`) que você não pode ler.
4. Se nada for encontrado, diga isso claramente. Não invente.

## 5. Log

Acrescente uma linha ao fim de `COFRE/_sistema/log/triagem-<aaaa-mm>.md`. Se o arquivo não existir, crie-o com o cabeçalho:

```
| data | fonte | resumo (1 linha) | destino | motivo | nota |
|---|---|---|---|---|---|
| aaaa-mm-dd | conversa | <resumo sem dado sigiloso> | ARMAZENAR/FUNDIR/INBOX/DESCARTAR | <motivo> | [[<nota>]] ou — |
```

## 6. Resposta ao usuário

Uma ou duas linhas por item, com destino, motivo e link da nota. Exemplo:
> **ARMAZENAR** · lição nova, a causa raiz vale para outras reindexações → [LIC-2026-10-22-timeout-na-reindexacao](...)

Se mascarou algo, diga o quê (o tipo, nunca o valor).

## 7. Fazer aqui ou delegar ao agente `segundo-cerebro`

| Situação | Onde |
|---|---|
| Uma captura rápida, ou uma consulta pontual | **Aqui**, na própria conversa |
| Lote (várias lições ou decisões), revisão da Inbox, consolidação de duplicatas, consulta ampla | **Agente** `segundo-cerebro`, para não encher esta conversa |

O agente **não vê esta conversa**. Ao delegar:
1. Monte a lista aqui e confirme com o usuário (§3.5).
2. Passe no prompt, para cada item: tipo; título; o que aconteceu; **cada tentativa, com o resultado e por que falhou**; causa raiz; solução; `situacao`; sistema, componentes ou tabelas; IDs de demanda. Escreva já sem dado de contribuinte.
3. Diga explicitamente "lista aprovada pelo usuário".
4. Confira o relatório do agente e repasse ao usuário os links das notas.
