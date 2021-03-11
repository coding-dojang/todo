import os
import unittest

from main import (add_task, list_task, get_last_index, make_it_done,
                  save_task, Task, TaskStatus)

class TaskTest(unittest.TestCase):
    def setUp(self):
        self.file_name = 'test_tasks.txt'

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_add_task(self):
        expected_results = ['0,todo,task1\n', '1,todo,task2\n']
        tasks = ['task1', 'task2']
        for task in tasks:
            add_task(task, self.file_name)
        test_file = open(self.file_name, 'r')
        self.assertEqual(expected_results, test_file.readlines())

    def test_list_task(self):
        expected_tasks = [
            Task(status=TaskStatus.TODO, name='task one', index=0),
            Task(status=TaskStatus.TODO, name='task two', index=1),
            Task(status=TaskStatus.TODO, name='task three', index=2),
        ]

        input_tasks = ['task one', 'task two', 'task three']
        for task in input_tasks:
            add_task(task, self.file_name)
        actual_tasks = list_task(self.file_name)
        self.assertEqual(expected_tasks, actual_tasks)

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
         
    def test_make_it_done(self):
        input_tasks = ['task one', 'task two', 'task three']
        for task in input_tasks:
            add_task(task, self.file_name)
        make_it_done(1, self.file_name)
        tasks = list_task(self.file_name)
        self.assertEqual(tasks[0].status, TaskStatus.TODO)
        self.assertEqual(tasks[1].status, TaskStatus.DONE)

    def test_save_task_write_mode(self):
        # mode: write
        expected_tasks = [
            Task(status=TaskStatus.TODO, name='task1'),
            Task(status=TaskStatus.TODO, name='task1')
        ]
        expected_result = [
            f"{i},{task.status},{task.name}\n"
            for i, task
            in enumerate(expected_tasks)
        ]
        save_task(tasks=expected_tasks, file_name=self.file_name)
        with open(self.file_name, 'r') as f:
            self.assertEqual(f.readlines(), expected_result)
        
        # mode: append
        additional_tasks = [
            Task(status=TaskStatus.TODO, name='task1'),
            Task(status=TaskStatus.TODO, name='task1')
        ]
        additional_expected_result = [
            f"{i},{task.status},{task.name}\n"
            for i, task
            in enumerate(expected_tasks + additional_tasks)
        ]
        save_task(tasks=additional_tasks, is_append=True, file_name=self.file_name)
        with open(self.file_name, 'r') as f:
            self.assertEqual(f.readlines(), additional_expected_result)

    @unittest.skip('until implement new list_task') 
    def test_remove_task(self):
        tasks = [
            {'status': 'todo', 'name': 'task1'},
            {'status': 'todo', 'name': 'task1'},
        ]
        save_task(tasks, file_name=self.file_name)
        indexed_task = list_task
