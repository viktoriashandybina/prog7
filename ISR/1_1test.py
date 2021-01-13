import unittest
import main

class MainTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(main.matrix_multiply([[1,2],[3,4]],[[4,3],[2,1]]),[[8,5],[20,13]])

    def test_2(self):
        self.assertEqual(main.matrix_multiply([[5,6],[7,8]],[[8,7],[6,5]]),[[76,65],[104,89]])

    def test_3(self):
        self.assertEqual(main.matrix_multiply([[1,2],[3,4]],[[1,2,3]]),None)

    def test_4(self):
        self.assertEqual(main.matrix_multiply([[3,2,1]],[[4,3],[2,1]]),None)

if __name__ == '__main__':
    unittest.main()