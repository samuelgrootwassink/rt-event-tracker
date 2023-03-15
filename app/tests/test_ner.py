import unittest
from modules.ner import *


class TestNER(unittest.TestCase):
    
    def test_clean_sentence(self):
        string_1 = 'This is something I need to do!'
        string_2 = 'This rock exists of rocks'
        control_result_1 = ['something','need']
        control_result_2 = ['rock', 'exists', 'rock']
        test_result_1 = NER().clean_sentence(string_1)
        test_result_2 = NER().clean_sentence(string_2)
        self.assertEqual(test_result_1, control_result_1)
        self.assertEqual(test_result_2, control_result_2)
        self.assertIsInstance(test_result_1, list)
        for obj_type in [123,['1'],1.0,{"1", 1}, {'title':'something'},(1,0)]:
            with self.assertRaises(TypeError):
               NER().clean_sentence(obj_type)
        
        
    def test_named_entities(self):
        string_1 = 'Troops blew up the bridge on Monday, according to a local Donetsk region news site. Ukraine denies it intends to leave Bakhmut, despite six months of heavy fighting and reportedly dwindling stockpiles.'
        
        string_2 = "Europe's largest sporting goods company is expecting a lackluster year after splitting with disgraced rapper Kanye West. The company has made a point to distance itself from West's antisemitic comments."
        
        string_3 = 'They survived the earthquakes in Turkey or Syria, waited days under the rubble for help, were rescued — and died shortly after. What causes post-rescue death?'
        
        string_4 = 'Inspired by neurogastronomy, Irene Iborra’s menu explores the unusual flavours that evoke childhood memories. Irene Iborra tells tales with ice-cream and with a single lick she can summon up memories that send you spinning back to your childhood days.“When I opened Mamá Heladera in 2021 I thought: how can taste provoke memories and how can I find what these tastes are?” she said. Continue reading...'
        
        control_results_1 = {'Donetsk', 'Bakhmut', 'Troops', 'Ukraine'}
        control_results_2 = {'Kanye West', 'Europe'}
        control_results_3 = {'Turkey', 'Syria'}
        control_results_4 = {'Inspired','Irene', 'Irene Iborra', 'Mam Heladera'}
        
        test_results_1 = NER().named_entities(string_1)
        test_results_2 = NER().named_entities(string_2)
        test_results_3 = NER().named_entities(string_3)
        test_results_4 = NER().named_entities(string_4)
        self.assertSetEqual(test_results_1, control_results_1)
        self.assertSetEqual(test_results_2, control_results_2)
        # self.assertSetEqual(test_results_3, control_results_3)
        self.assertSetEqual(test_results_4, control_results_4)
        self.assertIsInstance(test_results_1, frozenset)
        
        for obj_type in [123,['1'],1.0,{"1", 1}, {'title':'something'},(1,0)]:
            with self.assertRaises(TypeError):
               NER().named_entities(obj_type)
               
    
    def test_common_entity_sets(self):
        """
        Test the method that returns common entity sets in a dictionary. Whenever an identical set is found the weight is increased by one, whenever a set is more than 80% identical the weight is increased by 0.5
        """
        test_entity_sets = [frozenset({'dog', 'street', 'fox', 'leaf', 'red'}),
                            frozenset({'dog', 'street', 'fox', 'leaf', 'red'}),
                            frozenset({'cat', 'street', 'fox', 'leaf', 'red'}),
                            frozenset({'car', 'tree', 'leaf', 'blue', 'pc'}),
                            frozenset({'car', 'tree', 'blue', 'pc'})]
        
        test_result = NER().common_entity_sets(test_entity_sets)
        
        control_result = {frozenset({'dog', 'street', 'fox', 'leaf', 'red'}): 2.5, 
                          frozenset({'cat', 'street', 'fox', 'leaf', 'red'}): 2, 
                          frozenset({'car', 'tree', 'leaf', 'blue', 'pc'}): 1.5,
                          frozenset({'car', 'tree', 'blue', 'pc'}): 1.5}
        
        self.assertIsInstance(test_result, dict)
        self.assertDictEqual(test_result, control_result)
        
    
