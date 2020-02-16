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


def main():
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
        print('{} does not exist, running mkdir\n'.format(REPOS_PATH))
        os.system('mkdir {}'.format(REPOS_PATH))

    repos_list = glob.glob(REPOS_PATH + '/*')

    for key in repos.keys():
        path = REPOS_PATH + '/' + key.replace('/', '_')
        if path not in repos_list:
            clone = 'git clone ' + repos[key] + ' {}'.format(path)
            os.system(clone)
            scan_repository(path)
        else:
            msg = '"{}" already exists!!'.format(key)
            print(msg)
        print('')


def scan_repository(repo):
    print('Scanning repository')
    codes = get_code_list(repo)
    for c in codes:
        grep_source(c)


def grep_source(path):
    with open(path) as f:
        print('Scanning {}'.format(path.replace(REPOS_PATH, '')))
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


if __name__ == "__main__":
    main()
