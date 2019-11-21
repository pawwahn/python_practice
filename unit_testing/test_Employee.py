
import unittest
from unit_testing import Employee
import os
print(os.getcwd())

class TestEmployee(unittest.TestCase):
    print("--------------------->>>>")

    @classmethod
    def setUpClass(cls):
        print(" \n Setup class method")

    @classmethod
    def tearDownClass(cls):
        print(" \n Teardown class method")

    def setUp(self):
        print("setUp function")
        self.emp1 = Employee.Employee('Pavan', 'Kota', 100)
        self.emp2 = Employee.Employee('Kumar', 'Kota', 200)

    def tearDown(self):
        print("tearDown function")

    def test_email(self):
        print(" \n 1st func - test email")
        self.assertEqual(self.emp1.email,'PavanKota@email.com')
        self.assertEqual(self.emp2.email, 'KumarKota@email.com')

    def test_fullname(self):
        print("\n 2nd func - test full name")
        self.assertEqual(self.emp1.full_name,'PavanKota')

    def test_apply_raise(self):
        print(" \n 3rd func - test apply raise")
        x = self.emp1.apply_raise()
        self.assertEqual(x,105)

        y = self.emp2.apply_raise()
        self.assertEqual(y,210)


if __name__=='__main__':
    unittest.main()


