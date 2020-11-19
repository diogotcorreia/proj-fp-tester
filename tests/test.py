
import unittest
import sys
import importlib
import os
from io import StringIO

target = importlib.import_module(sys.argv[1])


class TestEhTabuleiro(unittest.TestCase):
    def test_eh_tabuleiro1(self):
        """
        eh_tabuleiro(((1, 0, 0), (-1, 1, 0), (1, -1, -1))) = True
        """
        data = ((1, 0, 0), (-1, 1, 0), (1, -1, -1))
        result = target.eh_tabuleiro(data)
        self.assertEqual(result, True)

    def test_eh_tabuleiro2(self):
        """
        eh_tabuleiro(((1, 0, 0), ('0', 1, 0), (1, -1, -1))) = False
        """
        data = ((1, 0, 0), ('0', 1, 0), (1, -1, -1))
        result = target.eh_tabuleiro(data)
        self.assertEqual(result, False)

    def test_eh_tabuleiro3(self):
        """
        eh_tabuleiro(((1, 0, 0), (-1, 1, 0), (1, -1))) = False
        """
        data = ((1, 0, 0), (-1, 1, 0), (1, -1))
        result = target.eh_tabuleiro(data)
        self.assertEqual(result, False)

    def test_eh_tabuleiro4(self):
        """
        eh_tabuleiro(((True, 0, False), (-1, 1, True), (1, -1, False))) = False
        """
        data = ((True, 0, False), (-1, 1, True), (1, -1, False))
        result = target.eh_tabuleiro(data)
        self.assertEqual(result, False)

    def test_eh_tabuleiro5(self):
        """
        eh_tabuleiro(((1.0, 0, -1.0), (-1, 1, 0), (1, -1, 0))) = False
        """
        data = ((1.0, 0, -1.0), (-1, 1, 0), (1, -1, 0))
        result = target.eh_tabuleiro(data)
        self.assertEqual(result, False)

    def test_eh_tabuleiro6(self):
        """
        eh_tabuleiro(((1, 0, -1), "not a tuple", (1, -1, 0))) = False
        """
        data = ((1, 0, -1), "not a tuple", (1, -1, 0))
        result = target.eh_tabuleiro(data)
        self.assertEqual(result, False)

    def test_eh_tabuleiro7(self):
        """
        eh_tabuleiro("str") = False
        """
        data = "str"
        result = target.eh_tabuleiro(data)
        self.assertEqual(result, False)


class TestEscolherPosicaoManual(unittest.TestCase):
    def test_escolher_posicao_manual1(self):
        """
        escolher_posicao_manual('tabuleiro invalido')
        """
        with self.assertRaises(ValueError) as ctx:
            target.escolher_posicao_manual('tabuleiro_invalido')

        self.assertEqual(
            'escolher_posicao_manual: o argumento e invalido', str(ctx.exception))

    def test_escolher_posicao_manual2(self):
        """
        escolher_posicao_manual numa posicao ocupada
        """
        with self.assertRaises(ValueError) as ctx:
            sys.stdin = StringIO("2")
            sys.stdout = StringIO()
            target.escolher_posicao_manual(((0, 1, -1), (0, 0, 0), (0, 0, 0)))
            sys.stdout.close()
            sys.stdin.close()
            sys.stdout = sys.__stdout__
            sys.stdin = sys.__stdin__

        self.assertEqual(
            'escolher_posicao_manual: a posicao introduzida e invalida', str(ctx.exception))

    def test_escolher_posicao_manual3(self):
        """
        escolher_posicao_manual numa posicao fora do tabuleiro
        """
        with self.assertRaises(ValueError) as ctx:
            sys.stdin = StringIO("12")
            sys.stdout = StringIO()
            target.escolher_posicao_manual(((0, 1, -1), (0, 0, 0), (0, 0, 0)))
            sys.stdout.close()
            sys.stdin.close()
            sys.stdout = sys.__stdout__
            sys.stdin = sys.__stdin__

        self.assertEqual(
            'escolher_posicao_manual: a posicao introduzida e invalida', str(ctx.exception))

    def test_escolher_posicao_manual4(self):
        """
        escolher_posicao_manual retorna o valor com sucesso
        """
        sys.stdin = StringIO("4")
        sys.stdout = StringIO()
        result = target.escolher_posicao_manual(
            ((0, 1, -1), (0, 0, 0), (0, 0, 0)))
        sys.stdout.seek(0, 0)
        self.assertEqual(sys.stdout.read(),
                         'Turno do jogador. Escolha uma posicao livre: ')
        self.assertEqual(result, 4)
        sys.stdout.close()
        sys.stdin.close()
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__


class TestEscolherPosicaoAuto(unittest.TestCase):
    def test_escolher_posicao_auto1(self):
        """
        Testa a regra 1 (vitoria)
        tableiro = ((1,0,0), (0,1,0), (0,0,0))
        """
        data = ((1, 0, 0), (0, 1, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 9)

    def test_escolher_posicao_auto2(self):
        """
        Testa a regra 2 (bloqueio)
        tableiro = ((1,0,0), (0,1,0), (0,0,0))
        """
        data = ((1, 0, 0), (0, 1, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 9)

    def test_escolher_posicao_auto3(self):
        """
        Testa a regra 3 (bifurcacao)
        tableiro = ((0,0,0), (1,-1,-1), (0,0,1))
        """
        data = ((0, 0, 0), (1, -1, -1), (0, 0, 1))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 7)

    def test_escolher_posicao_auto4(self):
        """
        Testa a regra 4 (bloqueio de bifurcacao com numero bifurcacoes == 1)
        tableiro = ((0,0,0), (1,-1,-1), (0,0,1))
        """
        data = ((0, 0, 0), (1, -1, -1), (0, 0, 1))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 7)

    def test_escolher_posicao_auto5(self):
        """
        Testa a regra 4 (bloqueio de bifurcacao com numero bifurcacoes > 1)
        tableiro = ((-1,0,0), (0,1,0), (0,0,1))
        """
        data = ((-1, 0, 0), (0, 1, 0), (0, 0, 1))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 3)

    def test_escolher_posicao_auto6(self):
        """
        Testa a regra 5 (centro)
        tableiro = ((0,0,0), (0,0,0), (0,0,0))
        """
        data = ((0, 0, 0), (0, 0, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 5)

    def test_escolher_posicao_auto7(self):
        """
        Testa a regra 6 (canto oposto)
        tableiro = ((0,0,0), (0,-1,0), (0,0,1))
        """
        data = ((0, 0, 0), (0, -1, 0), (0, 0, 1))

        result = target.escolher_posicao_auto(data, -1, 'normal')

        self.assertEqual(result, 1)

    def test_escolher_posicao_auto8(self):
        """
        Testa a regra 7 (canto vazio)
        tableiro = ((0,0,0), (0,-1,0), (0,0,1))
        """
        data = ((-1, 0, 0), (0, -1, 0), (0, 0, 1))

        result = target.escolher_posicao_auto(data, -1, 'basico')

        self.assertEqual(result, 3)

    def test_escolher_posicao_auto9(self):
        """
        Testa a regra 8 (lateral oposto)
        tableiro = ((-1,0,-1), (0,-1,0), (1,0,1))
        """
        data = ((-1, 0, -1), (0, -1, 0), (1, 0, 1))

        result = target.escolher_posicao_auto(data, -1, 'basico')

        self.assertEqual(result, 2)

    def test_escolher_posicao_auto115(self):
        """
        Teste 115 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
        """
        data = ((0, 0, 0), (0, 0, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'basico')

        self.assertEqual(result, 5)

    def test_escolher_posicao_auto116(self):
        """
        Teste 116 (escolher_posicao_auto)
        tabuleiro = ((1, 0, 0), (0, 0, 0), (0, 0, 0))
        """
        data = ((1, 0, 0), (0, 0, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, -1, 'basico')

        self.assertEqual(result, 5)

    def test_escolher_posicao_auto117(self):
        """
        Teste 117 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 0), (0, 1, 0), (0, 0, 0))
        """
        data = ((0, 0, 0), (0, 1, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, -1, 'basico')

        self.assertEqual(result, 1)

    def test_escolher_posicao_auto118(self):
        """
        Teste 118 (escolher_posicao_auto)
        tabuleiro = ((1, 0, 0), (0, -1, 0), (0, 0, 0))
        """
        data = ((1, 0, 0), (0, -1, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'basico')

        self.assertEqual(result, 3)

    def test_escolher_posicao_auto119(self):
        """
        Teste 119 (escolher_posicao_auto)
        tabuleiro = ((1, 0, 1), (0, -1, 0), (-1, 0, 0))
        """
        data = ((1, 0, 1), (0, -1, 0), (-1, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'basico')

        self.assertEqual(result, 9)

    def test_escolher_posicao_auto120(self):
        """
        Teste 120 (escolher_posicao_auto)
        tabuleiro = ((1, 0, 1), (0, 1, 0), (-1, 0, -1))
        """
        data = ((1, 0, 1), (0, 1, 0), (-1, 0, -1))

        result = target.escolher_posicao_auto(data, -1, 'basico')

        self.assertEqual(result, 2)

    def test_escolher_posicao_auto121(self):
        """
        Teste 121 (escolher_posicao_auto)
        tabuleiro = ((1, -1, 1), (0, -1, 0), (-1, 0, 1))
        """
        data = ((1, -1, 1), (0, -1, 0), (-1, 0, 1))

        result = target.escolher_posicao_auto(data, 1, 'basico')

        self.assertEqual(result, 4)

    def test_escolher_posicao_auto122(self):
        """
        Teste 122 (escolher_posicao_auto)
        tabuleiro = ((1, -1, 1), (1, -1, -1), (-1, 0, 1))
        """
        data = ((1, -1, 1), (1, -1, -1), (-1, 0, 1))

        result = target.escolher_posicao_auto(data, 1, 'basico')

        self.assertEqual(result, 8)

    def test_escolher_posicao_auto123(self):
        """
        Teste 123 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 0), (0, -1, 1), (1, 0, 0))
        """
        data = ((0, 0, 0), (0, -1, 1), (1, 0, 0))

        result = target.escolher_posicao_auto(data, -1, 'basico')

        self.assertEqual(result, 1)

    def test_escolher_posicao_auto124(self):
        """
        Teste 124 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
        """
        data = ((0, 0, 0), (0, 0, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'normal')

        self.assertEqual(result, 5)

    def test_escolher_posicao_auto125(self):
        """
        Teste 125 (escolher_posicao_auto)
        tabuleiro = ((0, 1, 0), (0, 0, 0), (0, 0, 0))
        """
        data = ((0, 1, 0), (0, 0, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, -1, 'normal')

        self.assertEqual(result, 5)

    def test_escolher_posicao_auto126(self):
        """
        Teste 126 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 0), (0, 1, 0), (0, 0, 0))
        """
        data = ((0, 0, 0), (0, 1, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, -1, 'normal')

        self.assertEqual(result, 1)

    def test_escolher_posicao_auto127(self):
        """
        Teste 127 (escolher_posicao_auto)
        tabuleiro = ((1, 0, 0), (0, -1, 0), (0, 0, 0))
        """
        data = ((1, 0, 0), (0, -1, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'normal')

        self.assertEqual(result, 3)

    def test_escolher_posicao_auto128(self):
        """
        Teste 128 (escolher_posicao_auto)
        tabuleiro = ((-1, 0, 0), (0, 1, 0), (0, 0, 0))
        """
        data = ((-1, 0, 0), (0, 1, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'normal')

        self.assertEqual(result, 9)

    def test_escolher_posicao_auto129(self):
        """
        Teste 129 (escolher_posicao_auto)
        tabuleiro = ((0, 0, -1), (0, 1, 0), (0, 0, 0))
        """
        data = ((0, 0, -1), (0, 1, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'normal')

        self.assertEqual(result, 7)

    def test_escolher_posicao_auto130(self):
        """
        Teste 130 (escolher_posicao_auto)
        tabuleiro = ((1, 0, 1), (0, -1, 0), (-1, 0, 0))
        """
        data = ((1, 0, 1), (0, -1, 0), (-1, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'normal')

        self.assertEqual(result, 2)

    def test_escolher_posicao_auto131(self):
        """
        Teste 131 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 1), (0, -1, 0), (-1, 0, 1))
        """
        data = ((0, 0, 1), (0, -1, 0), (-1, 0, 1))

        result = target.escolher_posicao_auto(data, 1, 'normal')

        self.assertEqual(result, 6)

    def test_escolher_posicao_auto132(self):
        """
        Teste 132 (escolher_posicao_auto)
        tabuleiro = ((1, 0, 0), (0, 1, 0), (-1, -1, 0))
        """
        data = ((1, 0, 0), (0, 1, 0), (-1, -1, 0))

        result = target.escolher_posicao_auto(data, 1, 'normal')

        self.assertEqual(result, 9)

    def test_escolher_posicao_auto133(self):
        """
        Teste 133 (escolher_posicao_auto)
        tabuleiro = ((1, 0, 0), (1, 0, 0), (0, -1, 0))
        """
        data = ((1, 0, 0), (1, 0, 0), (0, -1, 0))

        result = target.escolher_posicao_auto(data, -1, 'normal')

        self.assertEqual(result, 7)

    def test_escolher_posicao_auto134(self):
        """
        Teste 134 (escolher_posicao_auto)
        tabuleiro = ((1, 0, 1), (0, 0, 0), (0, -1, 0))
        """
        data = ((1, 0, 1), (0, 0, 0), (0, -1, 0))

        result = target.escolher_posicao_auto(data, -1, 'normal')

        self.assertEqual(result, 2)

    def test_escolher_posicao_auto135(self):
        """
        Teste 135 (escolher_posicao_auto)
        tabuleiro = ((1, -1, 1), (0, -1, 0), (0, 0, 0))
        """
        data = ((1, -1, 1), (0, -1, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'normal')

        self.assertEqual(result, 8)

    def test_escolher_posicao_auto136(self):
        """
        Teste 136 (escolher_posicao_auto)
        tabuleiro = ((1, 0, 1), (0, 1, 0), (-1, 0, -1))
        """
        data = ((1, 0, 1), (0, 1, 0), (-1, 0, -1))

        result = target.escolher_posicao_auto(data, -1, 'normal')

        self.assertEqual(result, 8)

    def test_escolher_posicao_auto137(self):
        """
        Teste 137 (escolher_posicao_auto)
        tabuleiro = ((1, -1, 1), (0, -1, 0), (-1, 0, 1))
        """
        data = ((1, -1, 1), (0, -1, 0), (-1, 0, 1))

        result = target.escolher_posicao_auto(data, 1, 'normal')

        self.assertEqual(result, 6)

    def test_escolher_posicao_auto138(self):
        """
        Teste 138 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 0), (0, -1, 1), (1, 0, 0))
        """
        data = ((0, 0, 0), (0, -1, 1), (1, 0, 0))

        result = target.escolher_posicao_auto(data, -1, 'normal')

        self.assertEqual(result, 3)

    def test_escolher_posicao_auto139(self):
        """
        Teste 139 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 0), (0, -1, 1), (0, 1, 0))
        """
        data = ((0, 0, 0), (0, -1, 1), (0, 1, 0))

        result = target.escolher_posicao_auto(data, -1, 'normal')

        self.assertEqual(result, 1)

    def test_escolher_posicao_auto140(self):
        """
        Teste 140 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 0), (0, 0, 0), (0, 1, 0))
        """
        data = ((0, 0, 0), (0, 0, 0), (0, 1, 0))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 5)

    def test_escolher_posicao_auto141(self):
        """
        Teste 141 (escolher_posicao_auto)
        tabuleiro = ((1, -1, 0), (0, 0, 0), (0, 0, 0))
        """
        data = ((1, -1, 0), (0, 0, 0), (0, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 5)

    def test_escolher_posicao_auto142(self):
        """
        Teste 142 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 0), (0, -1, 0), (1, 0, 0))
        """
        data = ((0, 0, 0), (0, -1, 0), (1, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 1)

    def test_escolher_posicao_auto143(self):
        """
        Teste 143 (escolher_posicao_auto)
        tabuleiro = ((1, 0, -1), (0, -1, 0), (1, 0, 0))
        """
        data = ((1, 0, -1), (0, -1, 0), (1, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 4)

    def test_escolher_posicao_auto144(self):
        """
        Teste 144 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 1), (0, 1, 0), (0, -1, -1))
        """
        data = ((0, 0, 1), (0, 1, 0), (0, -1, -1))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 7)

    def test_escolher_posicao_auto145(self):
        """
        Teste 145 (escolher_posicao_auto)
        tabuleiro = ((0, -1, 0), (0, 0, 0), (1, 0, 1))
        """
        data = ((0, -1, 0), (0, 0, 0), (1, 0, 1))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 8)

    def test_escolher_posicao_auto146(self):
        """
        Teste 146 (escolher_posicao_auto)
        tabuleiro = ((1, 0, 0), (-1, -1, 0), (1, 0, 0))
        """
        data = ((1, 0, 0), (-1, -1, 0), (1, 0, 0))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 6)

    def test_escolher_posicao_auto147(self):
        """
        Teste 147 (escolher_posicao_auto)
        tabuleiro = ((-1, 0, -1), (0, 1, 0), (1, 0, 1))
        """
        data = ((-1, 0, -1), (0, 1, 0), (1, 0, 1))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 2)

    def test_escolher_posicao_auto148(self):
        """
        Teste 148 (escolher_posicao_auto)
        tabuleiro = ((1, -1, 0), (0, 1, 0), (0, 0, -1))
        """
        data = ((1, -1, 0), (0, 1, 0), (0, 0, -1))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 4)

    def test_escolher_posicao_auto149(self):
        """
        Teste 149 (escolher_posicao_auto)
        tabuleiro = ((-1, 1, 0), (0, -1, 0), (0, 0, 1))
        """
        data = ((-1, 1, 0), (0, -1, 0), (0, 0, 1))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 3)

    def test_escolher_posicao_auto150(self):
        """
        Teste 150 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 0), (0, -1, 1), (1, 0, 0))
        """
        data = ((0, 0, 0), (0, -1, 1), (1, 0, 0))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 9)

    def test_escolher_posicao_auto151(self):
        """
        Teste 151 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 1), (0, -1, 0), (1, 0, 0))
        """
        data = ((0, 0, 1), (0, -1, 0), (1, 0, 0))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 2)

    def test_escolher_posicao_auto152(self):
        """
        Teste 152 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 0), (1, -1, -1), (0, 0, 1))
        """
        data = ((0, 0, 0), (1, -1, -1), (0, 0, 1))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 7)

    def test_escolher_posicao_auto153(self):
        """
        Teste 153 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 0), (-1, 1, 1), (0, 0, -1))
        """
        data = ((0, 0, 0), (-1, 1, 1), (0, 0, -1))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 7)

    def test_escolher_posicao_auto154(self):
        """
        Teste 154 (escolher_posicao_auto)
        tabuleiro = ((0, 0, 0), (0, -1, 1), (0, 1, 0))
        """
        data = ((0, 0, 0), (0, -1, 1), (0, 1, 0))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 9)

    def test_escolher_posicao_auto155(self):
        """
        Teste 155 (escolher_posicao_auto)
        tabuleiro = ((1, 0, 0), (0, 1, 0), (0, 0, -1))
        """
        data = ((1, 0, 0), (0, 1, 0), (0, 0, -1))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 3)

    def test_escolher_posicao_auto156(self):
        """
        Teste 156 (escolher_posicao_auto)
        tabuleiro = ((-1, 0, 0), (0, 1, -1), (0, 0, 1))
        """
        data = ((-1, 0, 0), (0, 1, -1), (0, 0, 1))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 7)

    def test_escolher_posicao_auto157(self):
        """
        Teste 157 (escolher_posicao_auto)
        tabuleiro = ((1, 0, 0), (0, -1, 1), (0, 0, -1))
        """
        data = ((1, 0, 0), (0, -1, 1), (0, 0, -1))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 2)


class TestJogoDoGalo(unittest.TestCase):
    def helper_jogo_do_galo(self, test_id, player, difficulty, expected_result):
        dirname = os.path.dirname(__file__)
        sys.stdin = open(os.path.join(
            dirname, 'testes_jogo_do_galo/test' + str(test_id) + '_input.txt'), 'r')
        response = StringIO()

        sys.stdout = response
        result = target.jogo_do_galo(player, 'perfeito')
        response.seek(0, 0)

        answer = open(os.path.join(
            dirname, 'testes_jogo_do_galo/test' + str(test_id) + '_answer.txt'), 'r')

        self.maxDiff = None
        self.assertEqual(answer.read(), response.read())
        self.assertEqual(expected_result, result)

        response.close()
        answer.close()
        sys.stdin.close()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def test_jogo_do_galo1(self):
        """                       
           |   |            |   |            O |   |          O |   |
        -----------      -----------        -----------      -----------
           |   |    ->      | X |      ->      | X |     ->     | X |
        -----------      -----------        -----------      -----------
           |   |            |   |              |   |            |   | X

         O |   | O        O | X | O          O | X | O        O | X | O         
        -----------      -----------        -----------      -----------
           | X |    ->      | X |      ->      | X |     ->     | X | X
        -----------      -----------        -----------      -----------
           |   | X          |   | X            | O | X          | O | X

         O | X | O        O | X | O            
        -----------      -----------   
         O | X | X  ->    O | X | X      
        -----------      -----------
           | O | X        X | O | X 

        """
        self.helper_jogo_do_galo(1, 'X', 'perfeito', 'EMPATE')

    def test_jogo_do_galo2(self):
        """                       
           |   |          X |   |            X |   |          X |   |
        -----------      -----------        -----------      -----------
           |   |    ->      |   |      ->      | O |     ->     | O |
        -----------      -----------        -----------      -----------
           |   |            |   |              |   |            |   | X

         X | O |          X | O |            X | O |          X | O | X 
        -----------      -----------        -----------      -----------
           | O |    ->      | O |      ->      | O |     ->     | O | 
        -----------      -----------        -----------      -----------  
           |   | X          | X | X          O | X | X        O | X | X

         X | O | X        X | O | X            
        -----------      -----------   
           | O | O  ->    X | O | O      
        -----------      -----------
         O | X | X        O | X | X 

        """
        self.helper_jogo_do_galo(2, 'X', 'perfeito', 'EMPATE')

    def test_jogo_do_galo3(self):
        """
           |   |            |   |            O |   |          O |   |
        -----------      -----------        -----------      -----------
           |   |    ->      | X |      ->      | X |     ->     | X |
        -----------      -----------        -----------      -----------
           |   |            |   |              |   |            |   | X

         O |   |          O |   | X          O |   | X 
        -----------      -----------        -----------
           | X |    ->      | X | O    ->      | X | O 
        -----------      -----------        ----------- 
           | O | X          | O | X          X | O | X 

        """
        self.helper_jogo_do_galo(3, 'O', 'perfeito', 'X')


class TestTabuleiroStr(unittest.TestCase):
    def test_tabuleiro_str1(self):

        data = ((1, -1, 0), (1, 0, -1), (1, -1, 0))

        result = target.tabuleiro_str(data)

        self.assertEqual(
            result, " X | O |   \n-----------\n X |   | O \n-----------\n X | O |   ")

    def test_tabuleiro_str_2(self):
        data = ((0, 0, 0), (0, 0, 0), (0, 0, 0))

        result = target.tabuleiro_str(data)

        self.assertEqual(
            result, "   |   |   \n-----------\n   |   |   \n-----------\n   |   |   ")

    def test_tabuleiro_str_3(self):
        data = ((1, 1, 1), (0, 0, 0), (-1, -1, -1))

        result = target.tabuleiro_str(data)

        self.assertEqual(
            result, " X | X | X \n-----------\n   |   |   \n-----------\n O | O | O ")

    def test_tabuleiro_str_4(self):
        data = ((1, 0, -1), (1, 0, -1), (1, 0, -1))

        result = target.tabuleiro_str(data)

        self.assertEqual(
            result, " X |   | O \n-----------\n X |   | O \n-----------\n X |   | O ")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'])
