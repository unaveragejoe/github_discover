from github import Github
import pickle
import numpy as np
import pandas as pd
import pickle as pickle
import pprint

from fake_useragent import UserAgent
import os
import requests
import time as time
import re
import random
import json
import urllib
import math

ua = UserAgent()

list_of_repos = pd.read_pickle('lst_of_repo_ids_and_commit_urls.pkl')

def get_commit_data(commit_link_list):
    commit_dict = {}
    
    z = requests.get('https://api.github.com/rate_limit').json()
    reset_time = z['resources']['core']['reset']
        
    for idx, repo in enumerate(commit_link_list):

        if reset_time >= math.floor(time.time()):
            time.sleep(60)
            z = requests.get('https://api.github.com/rate_limit').json()
            reset_time = z['resources']['core']['reset']
        
        headers = {'User-Agent': ua.random}
  
        response = requests.get(repo[1], headers)

        commits_json = json.loads(response.text)
        commit_dict[idx] = { 'id': repo[0],
                             'commits': commits_json }
        
        z = requests.get('https://api.github.com/rate_limit').json()
        reset_time = z['resources']['core']['reset']

        print(str(idx / len(commit_link_list)) + '%' + '\n')

        print(commit_dict[idx])

        with open('commit_dict.pkl', 'wb') as f:
            pickle.dump(commit_dict, f)
    return commit_dict

x = get_commit_data(list_of_repos)

with open('commit_dict_final.pkl', 'wb') as f:
    pickle.dump(x, f)