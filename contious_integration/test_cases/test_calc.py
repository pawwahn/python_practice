import unittest
from pytohn_practise.contious_integration.python_code import calc


class TestCalculator(unittest.TestCase):

    def test_addition(self):
        # print(calc.add(2, 2))
        print("<-- Inside test_addition function -->")
        self.assertEqual(calc.add(2, 2),4)


    def test_subtraction(self):
        print("<-- Inside test_subtraction function-->")
        self.assertEqual(calc.subtract(10, 5), 5)

    def test_prod(self):
        self.assertEqual(calc.prod(5, 3), 15)

    #


if __name__=='__main__':
    unittest.main()
