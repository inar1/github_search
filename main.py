#!/usr/bin/python3

import requests


SEARCH_API = 'https://api.github.com/search/repositories'


def main():
    res = requests.get(SEARCH_API)
    print(res)


if __name__ == "__main__":
    main()
