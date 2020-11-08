import unittest
import sys
import importlib

target = importlib.import_module(sys.argv[1])


class TestSum(unittest.TestCase):
    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]
        result = target.sum(data)
        self.assertEqual(result, 6)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'])
