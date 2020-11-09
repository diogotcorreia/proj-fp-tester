import unittest
import sys
import importlib

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


class TestJogoDoGalo(unittest.TestCase):
    def test_jogo_do_galo1(self):
        sys.stdin = open('testes_jogo_do_galo/test1_input.txt')
        result = open("testes_jogo_do_galo/my_out.txt", "w+")

        sys.stdout = result
        target.jogo_do_galo('X', 'perfeito')
        result.seek(0,0)

        answer = open('testes_jogo_do_galo/test1_answer.txt', 'r')

        self.maxDiff = None
        self.assertEqual(answer.read(), result.read())

        result.close()
        answer.close()    

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'])
