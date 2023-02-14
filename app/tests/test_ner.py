import unittest
from modules.ner import *


class TestNER(unittest.TestCase):
    
    def test_remove_stopwords(self):
        string = 'This is something I need to do!'
        control_results = 'something need !'
        test_results = NER()._remove_stopwords(string)
        
        self.assertEqual(test_results, control_results)
        self.assertIsInstance(test_results, str)
        for obj_type in [123,['1'],1.0,{"1", 1}, {'title':'something'},(1,0)]:
            with self.assertRaises(TypeError):
               NER()._remove_stopwords(obj_type)
        
        
    def test_named_entities(self):
        string_1 = 'Troops blew up the bridge on Monday, according to a local Donetsk region news site. Ukraine denies it intends to leave Bakhmut, despite six months of heavy fighting and reportedly dwindling stockpiles.'
        string_2 = 'As China on Sunday welcomes the Lunar New Year, many families are reuniting over the holidays for the first time since the Covid-19 crisis erupted. Following tough “Zero Covid” closures, China’s borders have been reopened this year, bringing festive cheer and a few emotional tears at border crossings'
        control_results_1 = {'Donetsk', 'Ukraine', 'Bakhmut', 'Troops'}
        control_results_2 = {'China', 'Lunar New Year', 'Zero Covid'}
        
        test_results_1 = NER().named_entities(string_1)
        test_results_2 = NER().named_entities(string_2)
        self.assertEqual(test_results_1, control_results_1)
        self.assertEqual(test_results_2, control_results_2)
        self.assertIsInstance(test_results_1, set)
        
        for obj_type in [123,['1'],1.0,{"1", 1}, {'title':'something'},(1,0)]:
            with self.assertRaises(TypeError):
               NER().named_entities(obj_type)