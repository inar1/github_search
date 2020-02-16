#!/usr/bin/python3

import requests
import datetime
import glob
import os


SEARCH_API = 'https://api.github.com/search/repositories'
CMDLINE_WIDTH = 80
REPOS_PATH = './data'
DURATION = 90
STARS = 100
EXTENSIONS = ['.php']
QUEUE_LENGTH = 5

GREP_FUNC = [
    'echo'
]


def main():
    print_title()

    today = datetime.date.today()
    past = today - datetime.timedelta(days=DURATION)

    api_params = '?q=web'
    api_params += '+language:{}'.format('php')
    api_params += '+stars:>{}'.format(STARS)
    api_params += '+pushed:{}'.format(past)

    res = requests.get(SEARCH_API + api_params)
    data = res.json()
    repos = {}
    for repo in data['items']:
        full_name = repo['full_name']
        repos[full_name] = repo['clone_url']

    if REPOS_PATH not in glob.glob('./*'):
        red_print('{} does not exist, running mkdir\n'.format(REPOS_PATH))
        os.system('mkdir {}'.format(REPOS_PATH))

    repos_list = glob.glob(REPOS_PATH + '/*')

    for key in repos.keys():
        path = REPOS_PATH + '/' + key.replace('/', '_')
        if path not in repos_list:
            clone = 'git clone ' + repos[key] + ' {}'.format(path)
            os.system(clone)
        else:
            msg = '"{}" already exists!!'.format(key)
            red_print(msg)

        scan_repository(key, path)
        print('')


def scan_repository(name, path):
    red_print('\n# Scanning repository {}...'.format(name))
    codes = get_code_list(path)
    red_print('# {} has {} files to be scanned...'.format(name, len(codes)))
    red_print('#' * CMDLINE_WIDTH + '\n')
    for c in codes:
        grep_source(c)


def grep_source(path):
    with open(path) as f:
        count = 1
        line_queue = []
        filename = path.replace(REPOS_PATH, '')
        print('Scanning {}...'.format(filename))
        line = f.readline()
        line_queue = insert(line_queue, line)
        if not line:
            red_print('No content in {}\n'.format(filename))
            return
        while line:
            line_queue = insert(line_queue, line)
            for func in GREP_FUNC:
                if func in line:
                    print_scan_result(line_queue, count)
            line = f.readline()
            count += 1


def insert(line_queue, new_item):
    if len(line_queue) >= QUEUE_LENGTH:
        line_queue.pop(0)
    line_queue.append(new_item)
    return line_queue


def print_scan_result(line_queue, line_num):
    queue_len = len(line_queue)
    for count, line in enumerate(line_queue):
        msg = str(line_num - queue_len + int(count) + 1) + ':' + '\t' + line
        print(msg, end="")
    print('')


def get_code_list(path):
    codes = []
    for x in glob.glob(path + '/**/*'):
        for ex in EXTENSIONS:
            if x.endswith(ex):
                codes.append(x)
    return codes


def red_print(strings):
    print('\033[31m' + strings + '\033[0m')


def print_title():
    print('\n' + '#' * CMDLINE_WIDTH)
    print('# Script started')
    print('#' * CMDLINE_WIDTH)


if __name__ == "__main__":
    main()
