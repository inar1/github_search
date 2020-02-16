#!/usr/bin/python3

import requests
import datetime
import glob
import os


SEARCH_API = 'https://api.github.com/search/repositories'
REPOS_PATH = './data'
DURATION = 90
STARS = 100
EXTENSIONS = ['.php']
CMDLINE_WIDTH = 50


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
            scan_repository(key, path)
        else:
            msg = '"{}" already exists!!'.format(key)
            red_print(msg)
        print('')


def scan_repository(name, path):
    print('\n# Scanning repository {}...'.format(name))
    codes = get_code_list(path)
    print('# Repository {} has {} files to be scanned...'.format(name,
                                                                 len(codes)))
    red_print('#' * CMDLINE_WIDTH + '\n')
    for c in codes:
        grep_source(c)


def grep_source(path):
    with open(path) as f:
        print('Scanning {}...'.format(path.replace(REPOS_PATH, '')))
        line = f.readline()
        while line:
            print(line)
            line = f.readline()
            break


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
    print('#' * CMDLINE_WIDTH)
    print('# Script started')
    print('#' * CMDLINE_WIDTH)


if __name__ == "__main__":
    main()
