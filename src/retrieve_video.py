import requests

sess=requests.Session()
sess.auth = ('96728-abb21-72de6-f4d08-ef5c1-e1e41', 'abf07-5cf6a-e236f-a98ec-8786f-30cf4')
response = sess.get('https://api.shutterstock.com/v2/images/search',
                    params={"query":input(),
                            'sort': 'popular'}
                    )
print(response.json())
