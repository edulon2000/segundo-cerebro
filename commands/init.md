---
description: Cria ou completa o cofre Obsidian do segundo cérebro e registra o caminho dele para a skill
argument-hint: "<pasta do cofre>"
allowed-tools: Bash, Read
---

Prepare o cofre do segundo cérebro na pasta: **$ARGUMENTS**

1. Se nenhuma pasta foi informada, pergunte ao usuário onde fica (ou deve ficar) o cofre do Obsidian e pare até ele responder.
2. Rode primeiro a simulação e mostre o resultado:
   `python "${CLAUDE_PLUGIN_ROOT}/scripts/init_cofre.py" --destino "<pasta>" --simular`
3. Se a pasta já tiver conteúdo, lembre que nada existente é sobrescrito: só o que falta é copiado. Peça o ok do usuário.
4. Com o ok, rode sem `--simular`.
5. Explique os próximos passos:
   - Abrir a pasta no Obsidian como cofre (ou recarregar o Obsidian, se ele já estiver aberto, para pegar a configuração de modelos e nota diária).
   - Em Configurações → Plugins principais, conferir que **Sync** está desligado, se os dados de trabalho não puderem sair da máquina.
   - Editar `_sistema/REGRAS.md` (lista de sistemas, ajustes de regras).
   - Para dicionários de dados: copiar `_sistema/config.exemplo.json` para `_sistema/config.json`, apontar as origens e rodar `python "<pasta>/_sistema/scripts/importar_dicionario.py"`.
   - A partir daí, em qualquer projeto: "guarda no cérebro: …" ou "registra no cérebro o que aprendemos hoje".
