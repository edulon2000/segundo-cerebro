"""Informa o caminho do cofre do segundo cérebro.

Ordem de busca:
1. variável de ambiente CEREBRO_COFRE;
2. chave "cofre" de ~/.claude/segundo-cerebro.json (gravada por /segundo-cerebro:init).

Imprime o caminho absoluto (com "/") e sai com 0; sem cofre configurado ou
com caminho inválido, explica o que fazer e sai com 1.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

CONFIG = Path.home() / ".claude" / "segundo-cerebro.json"


def localizar() -> Path | None:
    valor = os.environ.get("CEREBRO_COFRE")
    if not valor and CONFIG.exists():
        try:
            valor = json.loads(CONFIG.read_text(encoding="utf-8")).get("cofre")
        except ValueError:
            valor = None
    return Path(valor).expanduser().resolve() if valor else None


def main() -> int:
    cofre = localizar()
    if cofre is None:
        print("Nenhum cofre configurado. Rode /segundo-cerebro:init <pasta> ou defina CEREBRO_COFRE.")
        return 1
    if not (cofre / "_sistema" / "REGRAS.md").exists():
        print(f"O caminho configurado não parece um cofre (falta _sistema/REGRAS.md): {cofre.as_posix()}")
        return 1
    print(cofre.as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
