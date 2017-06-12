import unittest
import os.path
from app import *

class AppTestCase(unittest.TestCase):
    """Tests for `app.py`."""

    @classmethod
    def setUpClass(cls):
        add_entry("word","definition of the word")

    def test_empty_dictionary_created(self):
        self.assertTrue(os.path.isfile("gre_words.csv"))

    def test_blank_dictionary_initiated(self):
        file = open("gre_words.csv","r")
        line = file.readline()
        self.assertEqual("entry,definition",line.strip())
        file.close()

    def test_entry_added(self):
        file = open("gre_words.csv","r")
        file.readline()
        line = file.readline()
        self.assertEqual("word,definition of the word",line.strip())
        file.close()
    
    @classmethod
    def tearDownClass(cls):
        os.remove("gre_words.csv")

if __name__ == '__main__':
        unittest.main()
