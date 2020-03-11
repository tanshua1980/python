import re
import json
import time
import requests
from requests.exceptions import RequestException


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) '
            + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
    
    
def parse_one_page(html, start):
    #.*? 非贪婪匹配
    items1 = re.findall('href="(.*?)".*?title="(.*?)".*?', html)
    items2 = re.findall('pl">(.*?\/)?(.*?\/)?(.*?)\/(.*?)\/(.*?)<\/p>', html)#()?有的书没写作者
    items3 = re.findall('nums">(.*?)<\/span>.*?<\/div>(.*?)?<\/td>', html, re.S)#有的书没写书评
    #re.S使.匹配包括换行在内的所有字符
    for i in range(25):
        yield{
            #'page': start//25+1,
            #'ranking': start+i+1,
            #'book': 
            items1[i][1],
            'link': items1[i][0],
            
            'author': items2[i][0].replace('/', '').strip(),
            'press': items2[i][2].strip(),
            'time': items2[i][3].strip(),
            'price': items2[i][4].strip(),
            
            'grade': items3[i][0],
            #有书评的则要去除两边的源码
            'evaluation': items3[i][1].strip().replace("</span>\n              </p>", '')\
            .replace('<p class="quote" style="margin: 10px 0; color: #666">\n                  <span class="inq">', '') 
        }

def write_to_file(content):
    with open(r'C:\Users\TANSHUA\doubanBookTop250.txt', 'a+', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(start):
    url = 'https://book.douban.com/top250?start=' + str(start)
    html = get_one_page(url)
    for item in parse_one_page(html, start):
        #print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(start=i * 25)
        time.sleep(1)