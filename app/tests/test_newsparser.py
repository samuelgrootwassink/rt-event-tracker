import unittest
from modules.newsparser import *


class TestNewsParser(unittest.TestCase):
    

    def test_file_to_set(self):
        """
        Checks whether the text_to_set functions properly, leaves out any whitespaces and #comments. Also checks whether the correct type is returned
        """
        
        contol_results = {'https://test1.com','http://test2.org','www.test3.tech'}
        test_results = NewsParser().file_to_set('tests/test_files/test_file_to_set.txt')
        
        self.assertEqual(test_results, contol_results)
        self.assertIsInstance(test_results, set)
        with self.assertRaises(FileNotFoundError):
            NewsParser().file_to_set('app/non_existant_file.txt')


    # def test_parse_feed(self):
        
    #     test_results = NewsParser().parse_feed('tests/test_parse_feed.xml')
    #     control_results_1 = {
    #         'title':'test',
    #         'entries':[
    #             {
    #                 'title': 'test_1',
    #                 'summary':'summary of test'
    #             },
    #             {
    #                 'title': 'test_2',
    #                 'summary':'summary of test'
    #             }
    #         ]
    #     }
    #     self.assertEqual(test_results, control_results_1)
