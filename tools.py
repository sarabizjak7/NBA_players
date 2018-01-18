import requests
import os
import re
import string
import csv
import sys


nba_frontpage_url = 'http://en.hispanosnba.com/players/nba-all/index'
base_url = 'http://en.hispanosnba.com'
nba_directory = 'nba_dir'
html_filename = 'nba_list.html'

csv_filename = 'nba_list.csv'


def make_directory(filename):
    '''If not elready exist, create an empty directory for the given file'''
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(filename, exist_ok=True)


def save_page_to_file(url, filename, forced_download = False):
    '''Saves page on given url to given file'''
    try:
        print('Saving {}... '.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(filename) and not forced_download:
            print('Already saved')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('failed to connect to url' + url)
        return
    else:
        make_directory(filename)
        with open(filename, 'w', encoding='utf8') as f:
            f.write(r.text)
            print('Saved!')


def content_of_file(filename):
    '''Return string with content of given file'''
    with open(filename) as f:
        content = f.read()
    return content


def files(directory):
    '''Return names of all files in given directory and also a directory name'''
    return [os.path.join(directory, filename) for file in os.listdir(directory)]


def make_table(dictionaries, fields, filename):
    '''From a dictionary list make CSV file'''
    make_directory(filename)
    with open(filename, 'w', encoding='utf8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        for dictionary in dictionaries:
            writer.writerow(dictionary)

