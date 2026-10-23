"""Verificador de sigilo das notas do segundo cérebro (spec §10, decisões G1 e G5).

Procura CPF, CNPJ (numérico e alfanumérico), Inscrição Estadual da PB,
razão social, número de processo e segredos. Nunca imprime o valor
encontrado: só o tipo e a linha.

Uso:
    python verificar_sigilo.py ARQUIVO [ARQUIVO ...]             # só aponta
    python verificar_sigilo.py --mascarar ARQUIVO [ARQUIVO ...]  # mascara no lugar

Saída 0 = nada encontrado (ou tudo mascarado); 1 = há achados sem mascarar.
"""
import argparse
import re
import sys
from pathlib import Path


def _dv_mod11(valores, pesos):
    resto = sum(v * p for v, p in zip(valores, pesos)) % 11
    return 0 if resto < 2 else 11 - resto


def cpf_valido(texto: str) -> bool:
    d = [int(c) for c in re.sub(r"\D", "", texto)]
    if len(d) != 11 or len(set(d)) == 1:
        return False
    return (_dv_mod11(d[:9], range(10, 1, -1)) == d[9]
            and _dv_mod11(d[:10], range(11, 1, -1)) == d[10])


def cnpj_valido(texto: str) -> bool:
    """Vale para o CNPJ numérico e o alfanumérico (NT conjunta COCAD/SUARA/RFB nº 49/2024)."""
    c = re.sub(r"[^0-9A-Z]", "", texto.upper())
    if len(c) != 14 or not c[12:].isdigit() or len(set(c)) == 1:
        return False
    v = [ord(ch) - 48 for ch in c]
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1
    return _dv_mod11(v[:12], pesos1) == v[12] and _dv_mod11(v[:13], pesos2) == v[13]


def ie_pb_valida(texto: str) -> bool:
    d = [int(c) for c in re.sub(r"\D", "", texto)]
    if len(d) != 9 or d[:2] != [1, 6]:
        return False
    dv = 11 - sum(x * p for x, p in zip(d[:8], range(9, 1, -1))) % 11
    return (0 if dv >= 10 else dv) == d[8]


# (tipo, regex, validador ou None, máscara). Formatado = sempre mascara; sem máscara = só com DV válido.
REGRAS = [
    ("segredo", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"), None, "[segredo removido]"),
    ("segredo", re.compile(r"(?i)\b(senha|password|passwd|pwd|secret|token|api[_-]?key|x-redmine-api-key)\b(\s*[:=]\s*)(?!\[segredo removido\])[^\s,;]+"), None, r"\1\2[segredo removido]"),
    ("segredo", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9\-._~+/]{20,}=*"), None, "Bearer [segredo removido]"),
    ("segredo", re.compile(r"(?i)\bjdbc:[a-z0-9]+:[^\s]*(?:password=|/[^\s@]+@)[^\s]*"), None, "[conexão removida]"),
    ("CNPJ", re.compile(r"\b[0-9A-Z]{2}\.[0-9A-Z]{3}\.[0-9A-Z]{3}/[0-9A-Z]{4}-\d{2}\b"), None, "CNPJ ***"),
    ("CNPJ", re.compile(r"\b[0-9A-Z]{12}\d{2}\b"), cnpj_valido, "CNPJ ***"),
    ("CPF", re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"), None, "CPF ***"),
    ("CPF", re.compile(r"\b\d{11}\b"), cpf_valido, "CPF ***"),
    ("IE", re.compile(r"\b16\.\d{3}\.\d{3}-\d\b"), None, "IE ***"),
    ("IE", re.compile(r"\b16\d{7}\b"), ie_pb_valida, "IE ***"),
    ("processo", re.compile(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b"), None, "proc. ***"),
    ("processo", re.compile(r"(?i)\bproc(?:esso)?\.?\s*(?:n[º°o.]?\s*)?(?=[\d./-]*\d{4})[\d./-]{6,}\d"), None, "proc. ***"),
    ("razão social", re.compile(r"\b(?:[A-ZÀ-Ú0-9][\wÀ-ú&.\-]*\s+){1,6}(?:LTDA|S/A|S\.A\.|EIRELI|EPP|MEI)\b\.?"), None, "[contribuinte]"),
]


def analisar(texto: str):
    achados = []
    for tipo, regex, validador, _ in REGRAS:
        for m in regex.finditer(texto):
            if validador and not validador(m.group(0)):
                continue
            achados.append((texto.count("\n", 0, m.start()) + 1, tipo))
    return sorted(set(achados))


def mascarar(texto: str) -> str:
    for _, regex, validador, mascara in REGRAS:
        if validador:
            texto = regex.sub(lambda m: mascara if validador(m.group(0)) else m.group(0), texto)
        else:
            texto = regex.sub(mascara, texto)
    return texto


def main() -> int:
    # Console do Windows (cp1252) não imprime "→"; sem isto o script quebra justamente ao mascarar.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = argparse.ArgumentParser()
    args.add_argument("arquivos", nargs="+", type=Path)
    args.add_argument("--mascarar", action="store_true")
    opcoes = args.parse_args()

    pendente = False
    for arquivo in opcoes.arquivos:
        texto = arquivo.read_text(encoding="utf-8")
        achados = analisar(texto)
        if not achados:
            print(f"{arquivo.name}: ok")
            continue
        resumo = ", ".join(f"{tipo} (linha {linha})" for linha, tipo in achados)
        if opcoes.mascarar:
            arquivo.write_text(mascarar(texto), encoding="utf-8", newline="\n")
            restantes = analisar(arquivo.read_text(encoding="utf-8"))
            print(f"{arquivo.name}: mascarado → {resumo}")
            if restantes:
                pendente = True
                print(f"{arquivo.name}: AINDA HÁ ACHADOS → {restantes}")
        else:
            pendente = True
            print(f"{arquivo.name}: ACHADOS → {resumo}")
    return 1 if pendente else 0


if __name__ == "__main__":
    sys.exit(main())
