"""Testes do verificador de sigilo com documentos gerados (nunca reais)."""
import importlib.util
import random
import unittest
from pathlib import Path

CAMINHO = Path(__file__).resolve().parents[1] / "skills" / "segundo-cerebro" / "verificar_sigilo.py"
_spec = importlib.util.spec_from_file_location("verificar_sigilo", CAMINHO)
v = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v)


def gerar_cpf(rnd):
    d = [rnd.randint(0, 9) for _ in range(9)]
    d.append(v._dv_mod11(d, range(10, 1, -1)))
    d.append(v._dv_mod11(d, range(11, 1, -1)))
    return "".join(map(str, d))


def gerar_cnpj(rnd, alfanumerico):
    alfabeto = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" if alfanumerico else "0123456789"
    base = [rnd.choice(alfabeto) for _ in range(12)]
    valores = [ord(c) - 48 for c in base]
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    dv1 = v._dv_mod11(valores, pesos)
    dv2 = v._dv_mod11(valores + [dv1], [6] + pesos)
    return "".join(base) + f"{dv1}{dv2}"


def gerar_ie_pb(rnd):
    d = [1, 6] + [rnd.randint(0, 9) for _ in range(6)]
    dv = 11 - sum(x * p for x, p in zip(d, range(9, 1, -1))) % 11
    return "".join(map(str, d + [0 if dv >= 10 else dv]))


def formatar_cnpj(c):
    return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"


class TestVerificadorSigilo(unittest.TestCase):
    def setUp(self):
        rnd = random.Random(7)
        self.cpf = gerar_cpf(rnd)
        self.cnpj = gerar_cnpj(rnd, False)
        self.cnpj_alfa = gerar_cnpj(rnd, True)
        self.ie = gerar_ie_pb(rnd)

    def test_geradores_produzem_documentos_validos(self):
        self.assertTrue(v.cpf_valido(self.cpf))
        self.assertTrue(v.cnpj_valido(self.cnpj))
        self.assertTrue(v.cnpj_valido(self.cnpj_alfa))
        self.assertTrue(v.ie_pb_valida(self.ie))

    def test_detecta_cada_tipo(self):
        casos = {
            "CPF": [f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}", self.cpf],
            "CNPJ": [formatar_cnpj(self.cnpj), self.cnpj, formatar_cnpj(self.cnpj_alfa), self.cnpj_alfa],
            "IE": [self.ie, f"16.{self.ie[2:5]}.{self.ie[5:8]}-{self.ie[8]}"],
            "razão social": ["contribuinte DISTRIBUIDORA EXEMPLO DE ALIMENTOS LTDA autuado"],
            "segredo": ["senha=Abc123!", "X-Redmine-API-Key: 0123456789abcdef",
                        "jdbc:oracle:thin:usuario/segredo@host:1521/pdb"],
            "processo": ["processo nº 0012345/2024-7"],
        }
        for tipo, textos in casos.items():
            for texto in textos:
                with self.subTest(tipo=tipo, texto=texto):
                    self.assertIn(tipo, {t for _, t in v.analisar(f"x {texto} y")})

    def test_nao_pega_falsos_positivos(self):
        texto = ("issue #123456, commit 3f9a2c1b7e4d6a8f0b2c, versao 2026.11, "
                 "tabela TB_EXEMPLO_ITEM, contrato 001/2025, sprint SET/2025, numero 12345678901")
        self.assertEqual(v.analisar(texto), [])

    def test_mascarar_e_idempotente(self):
        texto = (f"CPF {self.cpf}, CNPJ {formatar_cnpj(self.cnpj_alfa)}, IE {self.ie}, "
                 "senha=Abc123!, EMPRESA EXEMPLO LTDA, processo nº 0012345/2024-7")
        mascarado = v.mascarar(texto)
        self.assertEqual(v.analisar(mascarado), [])
        self.assertEqual(v.mascarar(mascarado), mascarado)
        for valor in (self.cpf, self.cnpj_alfa, self.ie, "Abc123!"):
            self.assertNotIn(valor, mascarado)


if __name__ == "__main__":
    unittest.main()
