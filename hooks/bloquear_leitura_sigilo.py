"""Hook PreToolUse do plugin segundo-cerebro (regra G4).

Recusa chamadas de ferramenta cujo caminho ou comando cite as pastas do
cofre que guardam dados de trabalho sensíveis. Vale para qualquer cofre,
porque reconhece as pastas pelo nome. Complementa as regras deny do
.claude/settings.json do cofre, que não alcançam comandos de shell.

Se algo der errado (Python ausente, entrada inválida), o hook deixa passar:
num hook de usuário, falhar fechado travaria todas as sessões.
"""
import json
import re
import sys

PASTAS_PROTEGIDAS = ("10-Demandas", "21-Componentes", "_sistema/dados")

CAMPOS_POR_FERRAMENTA = {
    "Read": ("file_path",),
    "Edit": ("file_path",),
    "Write": ("file_path",),
    "Grep": ("path", "glob"),
    "Glob": ("path", "pattern"),
    "Bash": ("command",),
    "PowerShell": ("command",),
}

# Aceita "/" ou "\" (inclusive "\\") entre os segmentos e ignora caixa.
PADRAO = re.compile(
    "|".join(re.escape(p).replace("/", r"[\\/]+") for p in PASTAS_PROTEGIDAS),
    re.IGNORECASE,
)


def main() -> int:
    try:
        evento = json.load(sys.stdin)
    except ValueError:
        return 0

    campos = CAMPOS_POR_FERRAMENTA.get(evento.get("tool_name", ""), ())
    entrada = evento.get("tool_input") or {}
    texto = " ".join(str(entrada.get(c, "")) for c in campos)

    if PADRAO.search(texto):
        json.dump(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        "G4: o Claude Code não lê nem altera 10-Demandas, "
                        "21-Componentes ou _sistema/dados do segundo cérebro. "
                        "Peça só a saída agregada, ou o trecho necessário já sem dados sigilosos."
                    ),
                }
            },
            sys.stdout,
            ensure_ascii=True,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
