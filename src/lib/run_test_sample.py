import unittest

#  from test_example import MyClass

#  import random


class MyTest(unittest.TestCase):
    #  # Init the MyClass class
    #  my_class = MyClass()
    #
    #  # Database to verify test cases
    #  database = dict()

    def test_case_1(self):
        print("\n\nRunning Test 1....\n\n")
        name = 'John Doe'
        self.assertEqual(name, 'John Doe')
        print("\n\nFinished Test 1\n\n")


if __name__ == '__main__':
    # Run the main unittest code
    unittest.main()
