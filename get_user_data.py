from github import Github
import numpy as np
import pandas as pd
import pickle as pickle

import os
import requests
import time as time
import re
import random
import json
import math

g = Github("")

usernames = list(pd.read_pickle('all_contrib_usernames.pkl')['contributors'].values)

def get_user_data(lst_of_usernames):
    headers = {'authorization': ''}
    user_data = {}
        
    for idx, user_id in enumerate(lst_of_usernames):
        if g.rate_limiting[0] == 1 :
            time.sleep(3630)
              
        try:
            t1 = g.get_user(user_id)
            t2 = t1.raw_data
            t3 = list(t1.get_repos(user_id))
            t4 = [x.full_name for x in t3]
            r = [g.get_repo(x, headers).raw_data for x in t4]
#             print(t1,t2,t3,t4,r)
            
            user_data[user_id] = [t2, r]
            
            print(str(idx / len(lst_of_usernames)) + '%' + '\n')
            print('Number of queries remaining-->', g.rate_limiting[0])
            print(user_data[idx])
            
            with open(f'/user_data/user_data{idx}.pkl', 'wb') as f:
                pickle.dump({user_data[user_id]}, f)
            
        except:
            continue

        with open('user_data.pkl', 'wb') as f:
            pickle.dump(user_data, f)
            
    return user_data

    x = get_user_data(usernames)
