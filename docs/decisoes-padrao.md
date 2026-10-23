# Decisões-padrão (G1–G5)

São as decisões de governança com que o plugin vem configurado. Cada pessoa pode registrar as suas próprias no cofre (`40-Decisoes/`, modelo `decisao`) e ajustar `_sistema/REGRAS.md`.

| # | Decisão | Por quê | Onde está aplicada |
|---|---|---|---|
| **G1** | Dados de trabalho sigilosos **não** vão para LLM externo nem para o cofre. Só entra conhecimento técnico: causa raiz, abordagem, nome de classe ou tabela. | Tudo o que o Claude lê vai para o modelo. Dados de contribuinte são protegidos por sigilo fiscal. | `REGRAS.md` §1, skill §0, verificador de sigilo |
| **G2** | Cofre de trabalho separado do pessoal. | Para não prender a vida pessoal às restrições do trabalho, nem misturar dados fiscais com o resto. | Um cofre por `init`; `CEREBRO_COFRE` para alternar |
| **G3** | Cofre só na máquina local, sem Obsidian Sync. A reversibilidade vem de cópias de segurança, não de sincronização. | O Sync levaria os dados para fora da rede da organização. | `cofre-modelo/.obsidian/core-plugins.json` (`sync: false`) |
| **G4** | O Claude não lê nem altera `10-Demandas/`, `21-Componentes/` e `_sistema/dados/`. Pode linkar por ID. | São as pastas que recebem dados vindos dos sistemas de trabalho. | Hook do plugin e regras `deny` do cofre-modelo |
| **G5** | Número de processo é mascarado (`proc. ***`). | O número leva ao contribuinte. | Verificador de sigilo |

## Revisite estas decisões quando

- a sua organização publicar uma política sobre uso de IA;
- houver um LLM local aprovado, que permita resumos automáticos de dados de trabalho;
- for preciso acessar o cofre em outros dispositivos (aí vale repensar a G3 com uma opção dentro da rede).
