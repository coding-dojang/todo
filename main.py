'''
spec:
* CLI (command line interface)
* text
* list
* save
* add task

TODO:
[*] list - return tasks line by line
[*] add task
[*] change data structure
[*] add index
[*] done task
[*] save function
[*] remove task
[*] convert to OOP
[ ] make TaskManager use state more
[ ] modify task
[ ] undone task

'''
# data example
# 0,todo,"Go to zoo"
# 1,done,"Take shower"
import os
from typing import List, Iterable
from enum import Enum
from dataclasses import dataclass


SAVE_FILE = 'tasks.txt'

class TaskStatus(Enum):
    TODO = 'todo'
    DONE = 'done'

    def __str__(self):
        return str(self.value)
        
@dataclass
class Task:
    status: TaskStatus
    name: str
    index: int = None


class EmptyTaskException(Exception):
    pass
class TaskManager:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.tasks = self.load()

    # add
    def add(self, task_name: str):
        try:
            last_index = self._get_last_index_from_task()
            next_index = last_index + 1
        except EmptyTaskException:
            next_index = 0
        self.tasks += [Task(status=TaskStatus.TODO, name=task_name, index=next_index)]
        
    # remove
    def remove(self, index: int):
        # list_task
        # tasks = self.list()

        # remove from index
        new_tasks = (
            task for task in self.tasks
            if not task.index == index
        )
        # save_task
        self.tasks = new_tasks
        self._save(new_tasks)

    # done
    def done(self, index: int):
        tasks = self.load()
        tasks[index].status = TaskStatus.DONE
        # save_task(tasks, file_name=file_name)
        self._save(tasks)
    
    # load
    def load(self):
        if not os.path.exists(self.file_name):
            return []
        with open(self.file_name) as save_file:
            lines = [line.strip() for line in save_file]
            tasks = []
            for line in lines:
                fields = line.split(',')
                tasks.append(Task(status=TaskStatus(fields[1]), name=fields[2], index=int(fields[0])))
            self.tasks = tasks
        return tasks

    # _save
    def _save(self, tasks: List[Task], is_append: bool=False):
        '''
        {
            'status': 'todo',
            'name': 'task 1',
        }
        lines??? ????????? file_name??? lines??? ????????????.
        mode??? 'w', 'a'
        '''
        if not is_append:
            str_tasks = [
                f"{i},{task.status},{task.name}\n"
                for i, task
                in enumerate(tasks)
            ]
            with open(self.file_name, 'w') as f:
                f.writelines(str_tasks)

        if is_append:
            for task in tasks:
                if os.path.exists(self.file_name):
                    save_file = open(self.file_name, 'r')
                    last_index = self._get_last_index(save_file.readlines())
                    next_index = last_index + 1
                    save_file.close()
                else:
                    next_index = 0
                save_file = open(self.file_name, 'a')
                save_file.write(f"{next_index},{task.status},{task.name}\n")
                save_file.close()

    def save(self):
        self._save(self.tasks)

    def _get_last_index_from_task(self):
        if self.tasks == []:
            raise EmptyTaskException('empty list')
        return max([task.index for task in self.tasks])

    def _get_last_index(self, lines: list) -> int:
        # assume that index is sorted ascendingly
        if not lines:
            return 0
        return max([int(line.split(',')[0]) for line in lines])


if __name__ == '__main__':
    tm = TaskManager(SAVE_FILE)
    tm.add('hi')
    tm.add('hello')
    print(tm.load())