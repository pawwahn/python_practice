import unittest
from unit_testing import calculations

class TestCalc(unittest.TestCase):
    lst = [1,2,3,4]

    def test_squares(self):
        print("Inside test squares")
        result = calculations.squares(TestCalc.lst)
        self.assertEqual(result,[1,4,9,16])
        self.assertNotEqual(result, [1, 4, 9, 15])

    def test_cubes(self):
        print("Inside test cubes")
        result = calculations.cubes(TestCalc.lst)
        print(result)
        self.assertEqual(result,[1,8,27,64])

    def test_add_num(self):
        print("Inside add num")
        result = calculations.add_num(TestCalc.lst)
        print(result)
        self.assertEqual(result,10)

    def test_div(self):
        print("Inside test div")
        self.assertEqual(calculations.div(10,2),5)
        self.assertRaises(ValueError,calculations.div,10,0)
        print("--")
        self.assertNotEqual(calculations.div(10, 1), 2.5)
        with self.assertRaises(ValueError):
            calculations.div(10,0)

if __name__ =='__main__':
    TestCalc()