import unittest
from unit_testing import BasicFunction


class TestBasicFunction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUpclass method called** \n \n")

    @classmethod
    def tearDownClass(cls):
        print("tearDown class method called ** \n")

    def setUp(self):
        print("**setUp function called**")
        self.func = BasicFunction.BasicFunction()

    def tearDown(self):
        print("tearDown function called** \n")

    def test_1(self):
        print("Test1")
        self.assertTrue(True)

    def test_2(self):
        print("Test2")
        self.assertTrue(True)

    def test_3(self):
        print("Test3")
        self.assertEqual(self.func.state, 0)

    def test_4(self):
        print("Test4")
        self.func.increment_state()
        self.assertEqual(self.func.state, 1)

    def test_5(self):
        print("Test5")
        self.func.increment_state()
        self.func.increment_state()
        self.func.clear_state()
        self.func.increment_state()
        self.assertEqual(self.func.state, 1)


if __name__ == '__main__':
    unittest.main()