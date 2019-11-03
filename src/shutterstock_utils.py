from copy import copy
from typing import List
import random
import requests

sess=requests.Session()
sess.auth = ('96728-abb21-72de6-f4d08-ef5c1-e1e41', 'abf07-5cf6a-e236f-a98ec-8786f-30cf4')

def get_video(queries:List[str]):
    q=copy(queries)
    while q:
        response = sess.get('https://api.shutterstock.com/v2/videos/search',
                            params={'query':" ".join(q) + " NOT sad",
                                    'sort': 'relevance',
                                    'per_page': '5'}
                            )
        j=response.json()
        if 'data' in j:
            data=response.json()['data']
            if len(data)>0:
                qwwe=random.randrange(0,min(len(data),5))
                print("qwwe",qwwe)
                return data[qwwe]['assets']['preview_mp4']['url']
        del q[-1]
    return None