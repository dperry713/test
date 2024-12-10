import unittest

class TestNegativeSum(unittest.TestCase):
    def test_negative_sum(self):
        result = sum([-1, -2, -3])
        self.assertEqual(result, -6)

if __name__ == '__main__':
    unittest.main()
