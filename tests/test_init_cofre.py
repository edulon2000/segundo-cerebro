"""Testes do init do cofre e da localização do cofre pela skill.
O HOME é redirecionado para uma pasta temporária para não tocar na configuração real."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
INIT = RAIZ / "scripts" / "init_cofre.py"
COFRE_PY = RAIZ / "skills" / "segundo-cerebro" / "cofre.py"


class TestInitCofre(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.home = base / "home"
        self.cofre = base / "cofre"
        self.env = {**os.environ, "HOME": str(self.home), "USERPROFILE": str(self.home)}
        self.env.pop("CEREBRO_COFRE", None)

    def tearDown(self):
        self.tmp.cleanup()

    def rodar(self, *args):
        return subprocess.run([sys.executable, *map(str, args)], env=self.env,
                              capture_output=True, text=True, encoding="utf-8")

    def test_cria_cofre_e_registra_caminho(self):
        r = self.rodar(INIT, "--destino", self.cofre)
        self.assertEqual(r.returncode, 0, r.stderr)
        for caminho in ["_sistema/REGRAS.md", "_sistema/templates/licao.md", "Home.md",
                        ".claude/settings.json", ".obsidian/templates.json",
                        "50-Conhecimento/Licoes", "10-Demandas", "_sistema/log"]:
            self.assertTrue((self.cofre / caminho).exists(), caminho)
        config = json.loads((self.home / ".claude" / "segundo-cerebro.json").read_text(encoding="utf-8"))
        self.assertEqual(Path(config["cofre"]), self.cofre.resolve())

        r = self.rodar(COFRE_PY)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(Path(r.stdout.strip()), self.cofre.resolve())

    def test_nao_sobrescreve_o_que_existe(self):
        regras = self.cofre / "_sistema" / "REGRAS.md"
        regras.parent.mkdir(parents=True)
        regras.write_text("minhas regras", encoding="utf-8")
        r = self.rodar(INIT, "--destino", self.cofre)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(regras.read_text(encoding="utf-8"), "minhas regras")
        self.assertIn("_sistema/REGRAS.md", r.stdout)

    def test_simular_nao_grava(self):
        r = self.rodar(INIT, "--destino", self.cofre, "--simular")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(self.cofre.exists())
        self.assertFalse((self.home / ".claude" / "segundo-cerebro.json").exists())

    def test_sem_cofre_configurado_avisa(self):
        r = self.rodar(COFRE_PY)
        self.assertEqual(r.returncode, 1)
        self.assertIn("/segundo-cerebro:init", r.stdout)


if __name__ == "__main__":
    unittest.main()
