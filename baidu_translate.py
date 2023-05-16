import requests
from hashlib import md5
import random
import json
# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()
class baiduTranslate:
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
    
    def translate(self, query):
        from_lang = 'en'
        to_lang =  'zh'
        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        url = endpoint + path
        salt = random.randint(32768, 65536)
        sign = make_md5(self.app_id + query + str(salt) + self.app_key)
        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': self.app_id, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        # print(url)
        # Send request 
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()
        # Show response
        return result['trans_result'][0]['dst']
        