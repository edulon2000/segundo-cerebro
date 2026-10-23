"""Importa dicionários de dados em Markdown para 22-Banco/<schema>/.

Os dicionários de origem são pastas com `Tabelas/<TABELA>.md` (uma nota por
tabela, FKs como wikilinks) e alguns arquivos de índice na raiz. As origens
ficam em `_sistema/config.json`:

    {"dicionarios": {"meu-schema": "C:/caminho/do/dicionario"}}

O que o script faz:
- copia Tabelas/*.md mantendo os nomes;
- renomeia os demais .md com o prefixo "BD-<schema> — " e reescreve os wikilinks
  (evita links ambíguos quando dois dicionários têm arquivos de mesmo nome);
- acrescenta `tipo` e `schema` ao frontmatter;
- só grava o que mudou e remove do cofre o que sumiu da origem;
- aborta se algum nome colidir com outra nota do cofre.

Uso:
    python importar_dicionario.py [--schema <nome>] [--simular]
"""
import argparse
import json
import re
import sys
from pathlib import Path

COFRE = Path(__file__).resolve().parents[2]
DESTINO = COFRE / "22-Banco"
CONFIG = COFRE / "_sistema" / "config.json"

WIKILINK = re.compile(r"\[\[([^\]|#]+)([#|][^\]]*)?\]\]")
CORROMPIDO = "\ufffd"


def carregar_schemas() -> dict:
    if not CONFIG.exists():
        sys.exit(f"Falta {CONFIG}. Copie _sistema/config.exemplo.json para config.json e ajuste as origens.")
    dados = json.loads(CONFIG.read_text(encoding="utf-8")).get("dicionarios", {})
    return {nome: Path(origem) for nome, origem in dados.items()}


def novo_nome(schema: str, nome: str) -> str:
    """Nome no cofre de um arquivo que não é tabela."""
    if nome == "Dicionário de dados — Índice":
        return f"BD-{schema} — Índice"
    if nome.startswith("Índice — "):
        return f"BD-{schema} — Índice {nome[len('Índice — '):]}"
    return f"BD-{schema} — {nome}"


def com_frontmatter(texto: str, tipo: str, schema: str) -> str:
    extra = f"tipo: {tipo}\nschema: {schema}\n"
    if texto.startswith("---\n"):
        return "---\n" + extra + texto[4:]
    return "---\n" + extra + "---\n\n" + texto


def planejar(schema: str, origem: Path) -> dict:
    """Mapa caminho_no_cofre -> conteúdo, mais avisos."""
    if not origem.is_dir():
        sys.exit(f"Origem do schema {schema} não encontrada: {origem}")
    arquivos = sorted(origem.rglob("*.md"))
    renomes = {
        a.stem: novo_nome(schema, a.stem)
        for a in arquivos
        if a.parent.name != "Tabelas"
    }

    def trocar(m: re.Match) -> str:
        alvo = m.group(1).strip()
        return f"[[{renomes.get(alvo, alvo)}{m.group(2) or ''}]]"

    saida, corrompidos = {}, []
    for a in arquivos:
        texto = a.read_text(encoding="utf-8").replace("\r\n", "\n")
        e_tabela = a.parent.name == "Tabelas"
        texto = com_frontmatter(WIKILINK.sub(trocar, texto),
                                "tabela_bd" if e_tabela else "dicionario", schema)
        relativo = Path("Tabelas", a.name) if e_tabela else Path(renomes[a.stem] + ".md")
        saida[DESTINO / schema / relativo] = texto
        if CORROMPIDO in texto:
            corrompidos.append(a.stem)
    return {"arquivos": saida, "corrompidos": corrompidos}


def colisoes(planos: dict) -> list:
    """Nomes que já existem no cofre fora das pastas importadas."""
    alvos = {p for plano in planos.values() for p in plano["arquivos"]}
    existentes = {}
    for p in COFRE.rglob("*.md"):
        if DESTINO in p.parents or "_sistema" in p.parts or ".obsidian" in p.parts:
            continue
        existentes[p.stem.lower()] = p
    vistos, repetidos = {}, []
    for alvo in alvos:
        chave = alvo.stem.lower()
        if chave in existentes:
            repetidos.append(f"{alvo.stem} já existe em {existentes[chave]}")
        if chave in vistos:
            repetidos.append(f"{alvo.stem} aparece em dois schemas")
        vistos[chave] = alvo
    return sorted(repetidos)


def aplicar(schema: str, plano: dict, simular: bool) -> dict:
    pasta = DESTINO / schema
    novos = alterados = 0
    for caminho, texto in plano["arquivos"].items():
        atual = caminho.read_text(encoding="utf-8") if caminho.exists() else None
        if atual == texto:
            continue
        novos += atual is None
        alterados += atual is not None
        if not simular:
            caminho.parent.mkdir(parents=True, exist_ok=True)
            temporario = caminho.with_suffix(".md.tmp")
            temporario.write_text(texto, encoding="utf-8", newline="\n")
            temporario.replace(caminho)
    removidos = [p for p in pasta.rglob("*.md") if p not in plano["arquivos"]] if pasta.exists() else []
    if not simular:
        for p in removidos:
            p.unlink()
    return {"novos": novos, "alterados": alterados, "removidos": len(removidos)}


def main() -> int:
    schemas = carregar_schemas()
    args = argparse.ArgumentParser()
    args.add_argument("--schema", choices=sorted(schemas))
    args.add_argument("--simular", action="store_true")
    opcoes = args.parse_args()

    escolhidos = [opcoes.schema] if opcoes.schema else sorted(schemas)
    planos = {s: planejar(s, schemas[s]) for s in escolhidos}

    problemas = colisoes(planos)
    if problemas:
        print("Importação abortada, nomes repetidos:")
        print("\n".join(f"  - {p}" for p in problemas))
        return 1

    for schema, plano in planos.items():
        r = aplicar(schema, plano, opcoes.simular)
        tabelas = sum(1 for p in plano["arquivos"] if p.parent.name == "Tabelas")
        print(f"{schema}: {tabelas} tabelas, {len(plano['arquivos']) - tabelas} outras notas"
              f" | novos {r['novos']}, alterados {r['alterados']}, removidos {r['removidos']}"
              f"{' (simulação)' if opcoes.simular else ''}")
        if plano["corrompidos"]:
            print(f"  aviso: acentuação corrompida na origem em {', '.join(plano['corrompidos'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
