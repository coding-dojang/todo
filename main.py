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
[ ] done task
[ ] remove task
[ ] modify task

[ ] undone task

'''
# data example
# 0,"Go to zoo"
# 1,"Take shower"
import os


SAVE_FILE = 'tasks.txt'

def add_task(task: str, file_name: str = SAVE_FILE):
    if os.path.exists(file_name):
        save_file = open(file_name, 'r')
        last_index = get_last_index(save_file.readlines())
        next_index = last_index + 1
        save_file.close()
    else:
        next_index = 0
    save_file = open(file_name, 'a')
    save_file.write(f'{next_index},{task}\n')
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

if __name__ == '__main__':
    add_task('hi')
    add_task('hello')
    print(list_task())
