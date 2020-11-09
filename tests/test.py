
import unittest
import sys
import importlib
import os

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



class TestEscolherPosicaoAuto(unittest.TestCase):
    def test_escolher_posicao_auto1(self):
        """
        Testa a regra 1 (vitoria)
        tableiro = ((1,0,0), (0,1,0), (0,0,0))
        """
        data = ((1,0,0), (0,1,0), (0,0,0))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 9)

    def test_escolher_posicao_auto2(self):
        """
        Testa a regra 2 (bloqueio)
        tableiro = ((1,0,0), (0,1,0), (0,0,0))
        """
        data = ((1,0,0), (0,1,0), (0,0,0))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 9)

    def test_escolher_posicao_auto3(self):
        """
        Testa a regra 3 (bifurcacao)
        tableiro = ((0,0,0), (1,-1,-1), (0,0,1))
        """
        data = ((0,0,0), (1,-1,-1), (0,0,1))

        result = target.escolher_posicao_auto(data, 1, 'perfeito')

        self.assertEqual(result, 7)

    def test_escolher_posicao_auto4(self):
        """
        Testa a regra 4 (bloqueio de bifurcacao com numero bifurcacoes == 1)
        tableiro = ((0,0,0), (1,-1,-1), (0,0,1))
        """
        data = ((0,0,0), (1,-1,-1), (0,0,1))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 7)
 
    def test_escolher_posicao_auto5(self):
        """
        Testa a regra 4 (bloqueio de bifurcacao com numero bifurcacoes > 1)
        tableiro = ((-1,0,0), (0,1,0), (0,0,1))
        """
        data = ((-1,0,0), (0,1,0), (0,0,1))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 3)

    def test_escolher_posicao_auto6(self):
        """
        Testa a regra 5 (centro)
        tableiro = ((0,0,0), (0,0,0), (0,0,0))
        """
        data = ((0,0,0), (0,0,0), (0,0,0))

        result = target.escolher_posicao_auto(data, -1, 'perfeito')

        self.assertEqual(result, 5)
    
    def test_escolher_posicao_auto7(self):
        """
        Testa a regra 6 (canto oposto)
        tableiro = ((0,0,0), (0,-1,0), (0,0,1))
        """
        data = ((0,0,0), (0,-1,0), (0,0,1))

        result = target.escolher_posicao_auto(data, -1, 'normal')

        self.assertEqual(result, 1)

    def test_escolher_posicao_auto8(self):
        """
        Testa a regra 7 (canto vazio)
        tableiro = ((0,0,0), (0,-1,0), (0,0,1))
        """
        data = ((-1,0,0), (0,-1,0), (0,0,1))

        result = target.escolher_posicao_auto(data, -1, 'basico')

        self.assertEqual(result, 3)

    def test_escolher_posicao_auto9(self):
        """
        Testa a regra 8 (lateral oposto)
        tableiro = ((-1,0,-1), (0,-1,0), (1,0,1))
        """
        data = ((-1,0,-1), (0,-1,0), (1,0,1))

        result = target.escolher_posicao_auto(data, -1, 'basico')

        self.assertEqual(result, 2)


class TestJogoDoGalo(unittest.TestCase):
    def test_jogo_do_galo1(self):
        dirname = os.path.dirname(__file__)
        sys.stdin = open(os.path.join(
            dirname, 'testes_jogo_do_galo/test1_input.txt'))
        result = open(os.path.join(
            dirname, 'testes_jogo_do_galo/my_out.txt'), "w+")

        sys.stdout = result
        target.jogo_do_galo('X', 'perfeito')
        result.seek(0, 0)

        answer = open(os.path.join(
            dirname, 'testes_jogo_do_galo/test1_answer.txt'), 'r')

        self.maxDiff = None
        self.assertEqual(answer.read(), result.read())

        result.close()
        answer.close()
        sys.stdin.close()

    def test_jogo_do_galo2(self):
        dirname = os.path.dirname(__file__)
        sys.stdin = open(os.path.join(
            dirname, 'testes_jogo_do_galo/test2_input.txt'))
        result = open(os.path.join(
            dirname, 'testes_jogo_do_galo/my_out.txt'), "w+")

        sys.stdout = result
        target.jogo_do_galo('X', 'perfeito')
        result.seek(0, 0)

        answer = open(os.path.join(
            dirname, 'testes_jogo_do_galo/test2_answer.txt'), 'r')

        self.maxDiff = None
        self.assertEqual(answer.read(), result.read())

        result.close()
        answer.close()
        


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'])
