from copy import copy
from typing import List

import requests

sess=requests.Session()
sess.auth = ('96728-abb21-72de6-f4d08-ef5c1-e1e41', 'abf07-5cf6a-e236f-a98ec-8786f-30cf4')

def get_video(queries:List[str]):
    q=copy(queries)
    while q:
        response = sess.get('https://api.shutterstock.com/v2/videos/search',
                            params={'query':" ".join(q),
                                    'sort': 'random',
                                    'per_page': '1'}
                            )
        j=response.json()
        if 'data' in j:
            data=response.json()['data']
            if len(data)>0:
                return data[0]['assets']['preview_mp4']['url']
        del q[-1]
    return None