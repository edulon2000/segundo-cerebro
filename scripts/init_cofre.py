"""Cria (ou completa) um cofre do segundo cérebro a partir de cofre-modelo/.

- Copia os arquivos do modelo **sem sobrescrever** o que já existe no destino.
- Cria a estrutura de pastas.
- Grava o caminho do cofre em ~/.claude/segundo-cerebro.json, onde a skill o procura.

Uso:
    python init_cofre.py --destino "C:/Users/<voce>/Documents/Obsidian/MeuCofre" [--simular]
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

RAIZ_PLUGIN = Path(__file__).resolve().parents[1]
MODELO = RAIZ_PLUGIN / "cofre-modelo"
CONFIG = Path.home() / ".claude" / "segundo-cerebro.json"

PASTAS = [
    "00-Inbox", "10-Demandas", "20-Sistemas", "21-Componentes", "22-Banco",
    "30-Reunioes", "40-Decisoes", "50-Conhecimento/Conceitos", "50-Conhecimento/Fontes",
    "50-Conhecimento/Licoes", "60-Pessoas", "70-Projetos", "Diario", "MOCs",
    "_sistema/log", "_sistema/dados",
]


def main() -> int:
    args = argparse.ArgumentParser()
    args.add_argument("--destino", required=True, type=Path)
    args.add_argument("--simular", action="store_true")
    opcoes = args.parse_args()
    destino = opcoes.destino.expanduser().resolve()

    copiados, mantidos = [], []
    for origem in sorted(p for p in MODELO.rglob("*") if p.is_file()):
        relativo = origem.relative_to(MODELO)
        alvo = destino / relativo
        if alvo.exists():
            mantidos.append(relativo.as_posix())
            continue
        copiados.append(relativo.as_posix())
        if not opcoes.simular:
            alvo.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origem, alvo)

    if not opcoes.simular:
        for pasta in PASTAS:
            (destino / pasta).mkdir(parents=True, exist_ok=True)
        config = json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
        config["cofre"] = destino.as_posix()
        CONFIG.parent.mkdir(parents=True, exist_ok=True)
        CONFIG.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    sufixo = " (simulação)" if opcoes.simular else ""
    print(f"Cofre: {destino.as_posix()}{sufixo}")
    print(f"Copiados do modelo: {len(copiados)}")
    if mantidos:
        print(f"Já existiam e foram mantidos ({len(mantidos)}):")
        print("\n".join(f"  - {m}" for m in mantidos))
    if not opcoes.simular:
        print(f"Caminho do cofre gravado em {CONFIG.as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
