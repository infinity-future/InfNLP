
import json
import requests

ROOT = 'http://nlpapi.infuture.tech'


def tokenize(content):
    ret = requests.post(ROOT + '/hanlp/tokenize', json={
        'content': content
    }, timeout=30)
    ret = json.loads(ret.text)
    print(ret)


if __name__ == '__main__':
    tokenize('我爱北京天安门')
