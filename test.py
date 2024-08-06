import unittest
from src.frontend.app import get_index_title

class TestHelloApp(unittest.TestCase):

  def get_index_title(self):
    self.assertEqual(get_index_title(), "Demo Blog Website")

if __name__ == '__main__':
  unittest.main()
  