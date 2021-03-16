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
[ ] convert to OOP
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


class TaskManager:
    def __init__(self, file_name: str):
        self.file_name = file_name

    # add
    # remove
    # done
    # list

    # _save
    def _save(self, tasks: List[Task], is_append: bool=False):
        '''
        {
            'status': 'todo',
            'name': 'task 1',
        }
        lines를 받아서 file_name에 lines를 저장한다.
        mode는 'w', 'a'
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

    def _get_last_index(self, lines: list) -> int:
        # assume that index is sorted ascendingly
        if not lines:
            return 0
        return max([int(line.split(',')[0]) for line in lines])


def remove_task(index: int, file_name: str=SAVE_FILE):
    # list_task
    tasks = list_task(file_name)
    # remove from index
    new_tasks = (
        task for task in tasks
        if not task.index == index
    )
    # save_task
    save_task(tasks=new_tasks, file_name=file_name)


def save_task(tasks: List[Task], is_append: bool=False, file_name: str=SAVE_FILE) -> None:
    '''
    {
        'status': 'todo',
        'name': 'task 1',
    }
    lines를 받아서 file_name에 lines를 저장한다.
    mode는 'w', 'a'
    '''
    if not is_append:
        str_tasks = [
            f"{i},{task.status},{task.name}\n"
            for i, task
            in enumerate(tasks)
        ]
        with open(file_name, 'w') as f:
            f.writelines(str_tasks)

    if is_append:
        for task in tasks:
            if os.path.exists(file_name):
                save_file = open(file_name, 'r')
                last_index = get_last_index(save_file.readlines())
                next_index = last_index + 1
                save_file.close()
            else:
                next_index = 0
            save_file = open(file_name, 'a')
            save_file.write(f"{next_index},{task.status},{task.name}\n")
            save_file.close()


def add_task(task: str, file_name: str=SAVE_FILE):
    save_task(tasks=[Task(status=TaskStatus.TODO, name=task)], is_append=True, file_name=file_name)


def list_task(file_name: str = SAVE_FILE) -> List[Task]:
    save_file = open(file_name)
    lines = [line.strip() for line in save_file]
    tasks = []
    for line in lines:
        fields = line.split(',')
        tasks.append(Task(status=TaskStatus(fields[1]), name=fields[2], index=int(fields[0])))
    save_file.close()
    return tasks


def get_last_index(lines: list) -> int:
    # assume that index is sorted ascendingly
    if not lines:
        return 0
    return max([int(line.split(',')[0]) for line in lines])


def make_it_done(index: int, file_name: str = SAVE_FILE):
    '''
    status를 done으로 변경
    '''
    tasks = list_task(file_name)
    tasks[index].status = TaskStatus.DONE
    save_task(tasks, file_name=file_name)


if __name__ == '__main__':
    add_task('hi')
    add_task('hello')
    print(list_task())