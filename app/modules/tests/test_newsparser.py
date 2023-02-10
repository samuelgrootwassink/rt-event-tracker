import unittest
from modules.feedparser_lib import *

# parse feeds into dictionary


class TestNewsParser(unittest.TestCase):
    
    second
    def test_file_to_set(self):
        """
        Checks whether the text_to_set functions properly, leaves out any whitespaces and #comments. Also checks whether the correct type is returned
        """
        
        contol_results = set('https://test1.com','http://test2.org','www.test3.tech')
        test_results = NewsParser.file_to_set('app/modules/tests/test_files/test_file_to_set.txt')
        
        self.assertEqual(test_results, results)
        self.assertIsInstance(test_results, set)
        self.assertEqual(NewsParser.file_to_set('app/non_existant_file.txt'), FileNotFoundError)


    def test_parse_feed(self):
        
        test_results = NewsParser
        control_results_1 = {
            'title':'test_1',
            'entries':{
                'title': 'entry_1',
                'summary':'entry summary'
            }
        }
        self.assertEqual(first, results_1)
