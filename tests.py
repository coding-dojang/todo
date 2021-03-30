import os
import unittest

from main import Task, TaskStatus, TaskManager, EmptyTaskException

class TaskTest(unittest.TestCase):
    def setUp(self):
        self.file_name = 'test_tasks.txt'

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_add_task(self):
        expected_results = ['0,todo,task1\n', '1,todo,task2\n']
        tasks = ['task1', 'task2']
        tm = TaskManager(self.file_name)
        for task in tasks:
            tm.add(task)
        tm.save()
        with open(self.file_name, 'r') as test_file:
            self.assertEqual(expected_results, test_file.readlines())

    def test_list_task(self):
        expected_tasks = [
            Task(status=TaskStatus.TODO, name='task one', index=0),
            Task(status=TaskStatus.TODO, name='task two', index=1),
            Task(status=TaskStatus.TODO, name='task three', index=2),
        ]
        tm = TaskManager(self.file_name)

        input_tasks = ['task one', 'task two', 'task three']
        for task in input_tasks:
            tm.add(task)
        tm.save()
        actual_tasks = tm.load()
        self.assertEqual(expected_tasks, actual_tasks)

    def test_get_last_index(self):
        '''
        input: load (readlines()) -> csv like string
        parse csv like format 
        sorting
        get last index
        return last index
        '''
        lines = ['0,task1\n', '1,task2\n', '3,task4\n']
        expected_result = 3
        tm = TaskManager(self.file_name)
        actual_result = tm._get_last_index(lines)
        self.assertEqual(expected_result, actual_result)

    def test_get_last_index_with_comma_included_task(self):
        lines = ['0,task1\n', '1,"ta,sk2"\n']
        expected_result = 1
        tm = TaskManager(self.file_name)
        actual_result = tm._get_last_index(lines)
        self.assertEqual(expected_result, actual_result)

    def test_get_last_index_with_empty_list(self):
        lines = []
        expected_result = 0
        tm = TaskManager(self.file_name)
        actual_result = tm._get_last_index(lines)
        self.assertEqual(expected_result, actual_result)
         
    def test_make_it_done(self):
        input_tasks = ['task one', 'task two', 'task three']
        tm = TaskManager(self.file_name)
        for task in input_tasks:
            tm.add(task)
        tm.save()
        tm.done(1)
        tasks = tm.load()
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
        TaskManager(self.file_name)._save(tasks=expected_tasks)
        with open(self.file_name, 'r') as f:
            self.assertEqual(f.readlines(), expected_result)
        
        # mode: append
        additional_tasks = [
            Task(status=TaskStatus.TODO, name='task1'),
            Task(status=TaskStatus.TODO, name='task2')
        ]
        additional_expected_result = [
            f"{i},{task.status},{task.name}\n"
            for i, task
            in enumerate(expected_tasks + additional_tasks)
        ]
        TaskManager(self.file_name)._save(tasks=additional_tasks, is_append=True)
        # save_task(tasks=additional_tasks, is_append=True, file_name=self.file_name)
        with open(self.file_name, 'r') as f:
            self.assertEqual(f.readlines(), additional_expected_result)

    # @unittest.skip('until implement new list_task')
    @unittest.skip('until rename list() to load()')
    def test_remove_task(self):
        tasks = [
            Task(status=TaskStatus.TODO, name='task1'),
            Task(status=TaskStatus.TODO, name='task2')
        ]
        tm = TaskManager(self.file_name)
        # tm._save(tasks)
        for task in tasks:
            tm.add(task)
        tm.save()
        tm.remove(0)
        indexed_task = tm.load()
        self.assertEqual(len(indexed_task), 1)
        self.assertEqual(indexed_task[0].name, 'task2')

    #@unittest.skip('until rename list() to load()')
    def test_load_and_save_from_file(self):
        tasks = ['task1', 'task2']
        tm = TaskManager(self.file_name)
        load_tm = TaskManager(self.file_name)
        self.assertEqual(tm.tasks, load_tm.tasks)
        # tm._save(tasks)
        for task in tasks:
            tm.add(task)
        tm.save()
        # check save file

        load_tm.load()
        self.assertEqual(tm.tasks, load_tm.tasks)

        self.assertEqual(len(load_tm.tasks), 2)
        self.assertEqual(load_tm.tasks[0].name, 'task1')
        self.assertEqual(load_tm.tasks[1].name, 'task2')

    def test_list_without_save_file(self):
        tm = TaskManager(self.file_name)
        tasks = tm.load()
        self.assertEqual(tasks, [])
    
    def test_get_last_index_from_tasks(self):
        tm = TaskManager(self.file_name)
        LAST_INDEX_NUMBER = 10
        tasks = [
            Task(status=TaskStatus.TODO, name='task1', index=LAST_INDEX_NUMBER),
            Task(status=TaskStatus.TODO, name='task2', index=5)
        ]
        tm.tasks = tasks
        self.assertEqual(tm._get_last_index_from_task(), LAST_INDEX_NUMBER)

    def test_get_last_index_from_tasks_without_initial_data(self):
        '''
        get_last_index_from_tasks should raise EmptyTaskException when meet empty tasks list
        '''
        tm = TaskManager(self.file_name)
        self.assertRaises(EmptyTaskException, tm._get_last_index_from_task)
        tm.add('zero task')
        self.assertEqual(tm._get_last_index_from_task(), 0)
