"""Testes do hook de bloqueio G4. Os casos ficam aqui, não no comando, de propósito:
um hook ativo bloquearia um comando que citasse as pastas protegidas."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "bloquear_leitura_sigilo.py"
COFRE = "C:/Users/fulano/Documents/Obsidian/Cofre"


def decidir(ferramenta, campo, valor):
    entrada = json.dumps({"tool_name": ferramenta, "tool_input": {campo: valor}})
    saida = subprocess.run([sys.executable, str(HOOK)], input=entrada,
                           capture_output=True, text=True, check=True).stdout
    return "negar" if '"deny"' in saida else "permitir"


class TestHookG4(unittest.TestCase):
    def test_nega_pastas_protegidas(self):
        casos = [
            ("Read", "file_path", COFRE.replace("/", "\\") + "\\10-Demandas\\RM-1.md"),
            ("Edit", "file_path", COFRE + "/21-Componentes/sistema/CMP-a.md"),
            ("Grep", "path", COFRE + "/_sistema/dados"),
            ("Glob", "pattern", "**/21-Componentes/**"),
            ("Bash", "command", "cat " + COFRE + "/_sistema\\dados/relacoes.jsonl"),
            ("PowerShell", "command", "Get-Content " + COFRE + "/10-demandas/RM-2.md"),
        ]
        for caso in casos:
            with self.subTest(caso=caso):
                self.assertEqual(decidir(*caso), "negar")

    def test_permite_o_resto(self):
        casos = [
            ("Read", "file_path", "C:/projetos/app/src/Servico.java"),
            ("Write", "file_path", COFRE + "/50-Conhecimento/Licoes/LIC-x.md"),
            ("Read", "file_path", COFRE + "/22-Banco/schema/Tabelas/TB_X.md"),
            ("Grep", "pattern", "10-Demandas"),  # conteúdo buscado não é caminho
            ("Bash", "command", "git status"),
        ]
        for caso in casos:
            with self.subTest(caso=caso):
                self.assertEqual(decidir(*caso), "permitir")

    def test_entrada_invalida_deixa_passar(self):
        saida = subprocess.run([sys.executable, str(HOOK)], input="isto não é json",
                               capture_output=True, text=True, check=True).stdout
        self.assertEqual(saida, "")


if __name__ == "__main__":
    unittest.main()
