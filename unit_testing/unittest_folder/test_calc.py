import unittest
#from unit_testing.unittest_folder import calc
from . import calc


class TestCalc(unittest.TestCase):

    def test_add(self):
        self.assertEqual(calc.add(10, 5), 15)
        self.assertEqual(calc.add(10, -5), 5)
        self.assertEqual(calc.add(-10, -5), -15)
        self.assertEqual(calc.add(10,20), 30)

    def test_sub(self):
        self.assertEqual(calc.sub(10, 5), 5)
        self.assertEqual(calc.sub(10, -5), 15)
        self.assertEqual(calc.sub(-10, -5), -5)
        self.assertEqual(calc.sub(10,20), -10)

    def test_prod(self):
        self.assertEqual(calc.prod(-10, -5), 50)
        self.assertEqual(calc.prod(10,20), 200)
        self.assertEqual(calc.prod(10, 5), 50)
        self.assertEqual(calc.prod(10, -5), -50)

    def test_div(self):
        self.assertEqual(calc.div(-10, -5), 2)
        self.assertEqual(calc.div(10,20), 0.5)
        self.assertEqual(calc.div(10, 5), 2)
        self.assertEqual(calc.div(10, -5), -2)
        self.assertEqual(calc.div(10, -5), -2)
        # with self.assertRaises(ValueError):
        #     calc.div(10, 0)



if __name__=='__main__':
    unittest.main()