import unittest
from modules.newsparser import *


class TestNewsAggregator(unittest.TestCase):
    

    def test_file_to_set(self):
        """
        Checks whether the text_to_set functions properly, leaves out any whitespaces and #comments. Also checks whether the correct type is returned
        """
        
        contol_results = {'https://test1.com','http://test2.org','www.test3.tech'}
        test_results = NewsAggregator()._file_to_set('tests/test_files/test_file_to_set.txt')
        
        self.assertEqual(test_results, contol_results)
        self.assertIsInstance(test_results, set)
        with self.assertRaises(FileNotFoundError):
            NewsAggregator()._file_to_set('app/non_existant_file.txt')
            
        for obj_type in [123,['1'],1.0,{"1", 1}, {'title':'something'},(1,0)]:
            with self.assertRaises(TypeError):
                NewsAggregator()._file_to_set(obj_type)


    def test_parse_feed(self):
        """
        Checks whether feeds are parsed correctly and raise errors when needed
        """
        feed = NewsAggregator()._generate_feed('tests/test_files/test_parse_feed.xml')
        test_results = feed.to_dict()
        
        control_results_1 = {
            'title':'test',
            'language': 'en',
            'items':[
                {
                    'title': 'test_1',
                    'description':'summary of test'
                },
                {
                    'title': 'test_2',
                    'description':'summary of test'
                }
            ]
        }
        self.assertEqual(test_results, control_results_1)
        self.assertIsInstance(test_results, dict)
        
        with self.assertRaises(FileNotFoundError):
            NewsAggregator()._generate_feed('app/not_existing.xml')
        
        with self.assertRaises(Exception):
            NewsAggregator()._generate_feed('tests/test_files/test_parse_feed_unsuccesful.xml')
            
    
    # def test_aggregate(self):
        
    #     for obj_type in [123,['1'],1.0,{"1", 1}, {'title':'something'},(1,0)]:
    #         with self.assertRaises(TypeError):
    #             NewsAggregator().aggregate(obj_type)
                
    #     test_results = NewsAggregator()
    #     test_results.aggregate('tests/test_files/test_aggregate.txt')
        
    #     self.assertIsNotNone(test_results._feeds)
        
        
