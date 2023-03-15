import unittest
import xml.etree.ElementTree as ET
from modules.newsparser import *

RSS_FEED = 'tests/test_files/test_parse_feed_rss.xml'
RDF_FEED = 'tests/test_files/test_parse_feed_rdf.xml'
CONTROL_RESULTS_DICT = {
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
        rss_feed = NewsAggregator()._generate_feed(RSS_FEED)
        rdf_feed = NewsAggregator()._generate_feed(RDF_FEED)
        rss_test_results = rss_feed.to_dict()
        rdf_test_results = rdf_feed.to_dict()
    
        self.assertEqual(rss_test_results, CONTROL_RESULTS_DICT)
        self.assertEqual(rdf_test_results, CONTROL_RESULTS_DICT)
        self.assertIsInstance(rss_test_results, dict)
        
        with self.assertRaises(FileNotFoundError):
            NewsAggregator()._generate_feed('app/not_existing.xml')
        
        with self.assertRaises(Exception):
            NewsAggregator()._generate_feed('tests/test_files/test_parse_feed_unsuccesful.xml')
            
    
    def test_html_strip(self):
        
        test_results = NewsAggregator()._html_strip('hello how<a href="https//:example.net"> are you</a>')
        control_results = 'hello how are you'
        
        self.assertEqual(test_results, control_results)
    
    
    def test_is_url(self):
        test_result_1 = NewsAggregator()._is_url('hhhhttps woops//:')
        test_result_2 = NewsAggregator()._is_url('https://example.net')
        
        self.assertEqual(test_result_1, False)
        self.assertEqual(test_result_2, True)
    

    def test_parse_rss(self):
        
        rss_tree = ET.parse(RSS_FEED)
        rss_root = rss_tree.getroot()
        rss_feed = NewsAggregator()._parse_rss(rss_tree, rss_root)
        test_result = rss_feed.to_dict()
        
        self.assertEqual(test_result, CONTROL_RESULTS_DICT)
        self.assertIsInstance(rss_feed, Feed)
        

    def test_parse_rdf(self):
        
        rdf_tree = ET.parse(RDF_FEED)
        rdf_root = rdf_tree.getroot()
        rdf_feed = NewsAggregator()._parse_rdf(rdf_tree, rdf_root)
        test_result = rdf_feed.to_dict()
        
        self.assertEqual(test_result, CONTROL_RESULTS_DICT)
        self.assertIsInstance(rdf_feed, Feed)
        
    
    def test_parse_feed(self):
        
        path_options = {
            'title':['title','channel/title'],
            'language':['language', 'channel/language'],
            'items':['item', 'channel/item'],
            'item_title':['title'],
            'item_description':['description']
        }
        rss_tree = ET.parse(RSS_FEED)
        rss_root = rss_tree.getroot()
        rss_feed = NewsAggregator()._parse_feed(rss_tree, rss_root, path_options)
        test_result = rss_feed.to_dict()
        
        self.assertIsInstance(rss_feed, Feed)
        self.assertEqual(test_result, CONTROL_RESULTS_DICT)
        
    
    def tes_aggregate(self):
        pass
