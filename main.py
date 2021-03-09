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
[ ] save function
[ ] remove task
[ ] modify task

[ ] undone task

'''
# data example
# 0,todo,"Go to zoo"
# 1,done,"Take shower"
import os
from typing import List


SAVE_FILE = 'tasks.txt'

def save_task(tasks: List[dict], mode: str, file_name: str = SAVE_FILE) -> None:
    '''
    {
        'status': 'todo',
        'name': 'task 1',
    }
    lines를 받아서 file_name에 lines를 저장한다.
    mode는 'w', 'a'
    '''
    if mode == 'w':
        str_tasks = [
            f"{i},{task['status']},{task['name']}\n"
            for i, task
            in enumerate(tasks)
        ]
        with open(file_name, 'w') as f:
            f.writelines(str_tasks)

    if mode == 'a':
        for task in tasks:
            if os.path.exists(file_name):
                save_file = open(file_name, 'r')
                last_index = get_last_index(save_file.readlines())
                next_index = last_index + 1
                save_file.close()
            else:
                next_index = 0
            save_file = open(file_name, 'a')
            save_file.write(f"{next_index},{task['status']},{task['name']}\n")
            save_file.close()

def add_task(task: str, file_name: str = SAVE_FILE):
    if os.path.exists(file_name):
        save_file = open(file_name, 'r')
        last_index = get_last_index(save_file.readlines())
        next_index = last_index + 1
        save_file.close()
    else:
        next_index = 0
    save_file = open(file_name, 'a')
    save_file.write(f'{next_index},todo,{task}\n')
    save_file.close()

def list_task(file_name: str = SAVE_FILE) -> list:
    save_file = open(file_name)
    lines = [line.strip() for line in save_file]
    save_file.close()
    return lines

def get_last_index(lines: list) -> int:
    # assume that index is sorted ascendingly
    if not lines:
        return 0
    return max([int(line.split(',')[0]) for line in lines])

def make_it_done(index: int, file_name: str = SAVE_FILE):
    '''
    status를 done으로 변경
    '''
    lines = list_task(file_name)
    parsed_task = lines[index].split(',')
    parsed_task[1] = 'done'
    lines[index] = ','.join(parsed_task)
    with open(file_name, 'w') as save_file:
        for line in lines:
            save_file.write(line + '\n')

if __name__ == '__main__':
    add_task('hi')
    add_task('hello')
    print(list_task())
