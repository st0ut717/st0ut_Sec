import contextlib
import os
import queue
import requests
import sys
import threading
import time

filtered = ['.jpg', '.gif', '.png', '.css']
target = 'http://boodelyboo.com/wordpress'
threads = 10
answers = queue.Queue()
web_paths = queue.Queue()

def gather_paths():
    for root, _, files in os.walk('.'):
        for file_name in files:
            if os.path.splitext(file_name)[1] in filtered:
                continue
            path = os.path.join(root, file_name)
            if path.startswith('.'):
                path = path[1:]
            print(path)
            web_paths.put(path)

@contextlib.contextmanager
def chdir(path):
    """
    On enter cd to path
    on exit cd to org
    """
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)

if __name__ == '__main__':
    with chdir('/home/tim/Downloads/wordpress'):
        gather_paths()
    input('Press enter to continuw')



