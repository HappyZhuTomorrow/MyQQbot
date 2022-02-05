import requests
from urllib import parse
from bs4 import BeautifulSoup
import json
# lolname = '你好啊'
def chatBot(content):
    b = parse.quote(content)
    r = requests.get("https://api.ownthink.com/bot?appid=xiaosi&userid=user&spoken={}".format(b))
    data = json.loads(r.text)
    return data['data']['info']['text']
    print(data['data']['info']['text'])

if __name__ == '__main__':
    print(chatBot('你好啊'))