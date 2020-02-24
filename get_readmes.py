# from github import Github
import numpy as np
import pandas as pd
import pickle as pickle
# import pprint

from fake_useragent import UserAgent
import os
import requests
import time as time
import re
import random
import json
# import urllib
import math


ua = UserAgent()

list_of_content_pages = pd.read_pickle('lst_of_content_urls.pkl')

def get_readme_links(contents_links):
    contents_list = []
    
    z = requests.get('https://api.github.com/rate_limit').json()
    reset_time = z['resources']['core']['reset']
        
    for idx, repo in enumerate(lst_of_content_urls):
        if reset_time >= math.floor(time.time()):
            time.sleep(60)
            z = requests.get('https://api.github.com/rate_limit').json()
            reset_time = z['resources']['core']['reset']
        
        headers = {'User-Agent': ua.random}
        
        response = requests.get(repo[1], headers)
        response_json = json.loads(response.text)

        lst_of_filenames = [ doc["name"].lower() for idx, doc in enumerate(response_json) ]
        idx_of_readme = -1

        for i, x in enumerate(lst_of_filenames):
                if 'readme' in x:
                    idx_of_readme = i
                else:
                    continue
        try:
            contents_list.append([ repo[0], response_json[idx_of_readme]['download_url'] ])        
        except:
            contents_list.append([ repo[0], None])        
                
        z = requests.get('https://api.github.com/rate_limit').json()
        reset_time = z['resources']['core']['reset']
    
        print(str(idx / len(contents_links)) + '%' + '\n')

        print(contents_list[idx])
        with open('contents_list.pkl', 'wb') as f:
            pickle.dump(contents_list, f)

    return contents_list

    x = get_readme_links(list_of_content_pages)

    with open('contents_list_final.pkl', 'wb') as f:
            pickle.dump(x, f)