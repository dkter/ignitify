import requests

sess=requests.Session()
sess.auth = ('96728-abb21-72de6-f4d08-ef5c1-e1e41', 'abf07-5cf6a-e236f-a98ec-8786f-30cf4')

def get_video(query:str):
    response = sess.get('https://api.shutterstock.com/v2/videos/search',
                        params={'query':query,
                                'sort': 'relevance',
                                'per_page': '1'}
                        )
    data=response.json()['data']
    if len(data)>0:
        return data[0]['assets']['preview_mp4']['url']
    else:
        return 'https://billwurtz.com/snail-time.mp4'