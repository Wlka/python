import requests
import re
import urllib.request
import os
import datetime


def getPage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except:
        return "Error"


def parserHTML(html):
    formatTime = '%Y-%m-%d'
    Time = datetime.datetime.now().strftime(formatTime)
    name = ''
    imageurl = re.findall(r'<img src=.*/>', html)
    for i in range(len(imageurl)):
        imageurl[i] = imageurl[i].replace('<img src="', '')
        imageurl[i] = imageurl[i].replace('" style="display:none" onload="sc_lI();"/>', '')
        name = imageurl[i][16:]
        name = re.sub(r'\d*\_\d*x\d*', '', name)
        name = Time +'-'+ name
        print(name)
        imageurl[i] = 'https://cn.bing.com' + imageurl[i]
    return imageurl, name


def download(imageurl, name):
    #可修改下面三行os库的语句对下载目录进行修改
    if not os.path.exists('C:\\Users\\xxx\\Desktop\\bing'):
        os.mkdir('C:\\Users\\xxx\\Desktop\\bing')
    os.chdir('C:\\Users\\xxx\\Desktop\\bing')
    try:
        data = urllib.request.urlopen(imageurl).read()
        with open(name, "wb") as code:
            code.write(data)
        print('Done')
    except:
        print('Error')


def main():
    url = 'https://cn.bing.com/?mkt=zh-CN'
    html = getPage(url)
    list = parserHTML(html)
    download(list[0][0], list[1])
    os.system("pause")


if __name__ == "__main__":
    main()
