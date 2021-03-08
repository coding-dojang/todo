import os
import unittest

from main import add_task, list_task, get_last_index

class TaskTest(unittest.TestCase):
    def setUp(self):
        self.file_name = 'test_tasks.txt'

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_add_task(self):
        expected_results = ['0,task1\n', '1,task2\n']
        tasks = ['task1', 'task2']
        for task in tasks:
            add_task(task, self.file_name)
        test_file = open(self.file_name, 'r')
        self.assertEqual(expected_results, test_file.readlines())

    def test_list_task(self):
        expected_tasks = ['0,task one', '1,task two', '2,task three']

        input_tasks = ['task one', 'task two', 'task three']
        for task in input_tasks:
            add_task(task, self.file_name)
        actual_tasks = list_task(self.file_name)
        self.assertEqual(expected_tasks, actual_tasks)

    def test_done_task(self):
        pass

    def test_get_last_index(self):
        '''
        input: list (readlines()) -> csv like string
        parse csv like format 
        sorting
        get last index
        return last index
        '''
        lines = ['0,task1\n', '1,task2\n', '3,task4\n']
        expected_result = 3
        actual_result = get_last_index(lines)
        self.assertEqual(expected_result, actual_result)

    def test_get_last_index_with_comma_included_task(self):
        lines = ['0,task1\n', '1,"ta,sk2"\n']
        expected_result = 1
        actual_result = get_last_index(lines)
        self.assertEqual(expected_result, actual_result)

    def test_get_last_index_with_empty_list(self):
        lines = []
        expected_result = 0
        actual_result = get_last_index(lines)
        self.assertEqual(expected_result, actual_result)
         
        