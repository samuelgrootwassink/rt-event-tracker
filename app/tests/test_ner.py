# import unittest
# from modules.newsparser import *


# class TestNER(unittest.TestCase):
    

#     def test_file_to_set(self):
#         """
#         Checks whether the text_to_set functions properly, leaves out any whitespaces and #comments. Also checks whether the correct type is returned
#         """
        
#         contol_results = {'https://test1.com','http://test2.org','www.test3.tech'}
#         test_results = NewsAggregator()._file_to_set('tests/test_files/test_file_to_set.txt')
        
#         self.assertEqual(test_results, contol_results)
#         self.assertIsInstance(test_results, set)
#         with self.assertRaises(FileNotFoundError):
#             NewsAggregator()._file_to_set('app/non_existant_file.txt')
            
#         for obj_type in [123,['1'],1.0,{"1", 1}, {'title':'something'},(1,0)]:
#             with self.assertRaises(TypeError):
#                 NewsAggregator()._file_to_set(obj_type)
