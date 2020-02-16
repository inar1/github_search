#!/usr/bin/python3

import requests
import datetime
import glob
import os


SEARCH_API = 'https://api.github.com/search/repositories'
REPOS_PATH = './data'


def main():
    today = datetime.date.today()
    past = today - datetime.timedelta(days=30)

    api_params = '?q=web'
    api_params += '+language:{}'.format('php')
    api_params += '+stars:>{}'.format(100)
    api_params += '+pushed:{}'.format(past)

    res = requests.get(SEARCH_API + api_params)
    data = res.json()
    repos = {}
    for repo in data['items']:
        full_name = repo['full_name']
        repos[full_name] = repo['clone_url']

    print(glob.glob('./*'))
    if REPOS_PATH not in glob.glob('./*'):
        print('{} does not exist, running mkdir'.format(REPOS_PATH))
        os.system('mkdir {}'.format(REPOS_PATH))

    dir_list = glob.glob(REPOS_PATH + '/*')
    print(dir_list)

    for key in repos.keys():
        path = REPOS_PATH + '/' + key.replace('/', '_')
        if path not in dir_list:
            print('Cloning "{}"...'.format(key))
            clone = 'git clone ' + repos[key] + ' {}'.format(path)
            print(clone)
            os.system(clone)
        else:
            msg = '"{}" already exists!!'.format(key)
            print(msg)


if __name__ == "__main__":
    main()
