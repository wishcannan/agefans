from typing import Pattern
from bs4.element import SoupStrainer
import requests
import os
import json
import ast
from bs4 import BeautifulSoup
import re

from requests.api import post

class agefans():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}   # headers可以不用加,但加了总没错
        self.search_url = 'http://118.195.128.234:7788/ssszz.php?'
        self.js_url = 'http://d.gqyy8.com:8077/ne2/s{}.js?{}'
        self.index = 'http://agefans.top'

    def post_search(self,s):
        param = {
            'top':10,
            'q':s,
            'other_kkk217':'http://ysjdm8.com',
            'dect':0
        }
        r = requests.post(self.search_url,headers=self.headers,params=param)
        r.encoding = "utf-8"
        # state=json.loads(r.text)
        a = r.text.replace(' ','')
        # a = a.replace(']','}')
        # a = a.replace('[','{')
        return self.lo(a)
    def lo(self,s):
        flag = False
        p = ''
        alist = []
        for i in s:
            if i == '{':
                flag = True
            if i == '}':
                flag = False
                p += i
                alist.append(ast.literal_eval(p))
                p = ''
            if flag:
                p += i
        print(alist)
        return alist

    def download(self,url,file,title):
        print("开始下载"+title)
        size = 0
        if not os.path.exists(file):
            os.mkdir(file)
        r = requests.get(url,self.headers)
        if r.status_code == 200:
            chunk_size= 1024
            print(r.headers)
            content_size = int(r.headers['content-length'])
            # print(content_size)
            print('[文件总大小]:{:.0f} MB'.format(content_size / 1024 / 1024))
            with open(file+'/'+title+'.mp4','wb') as f:
                for data in r.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    size += len(data)
                    print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size*50/ content_size),float(size/content_size * 100)),end='\n')
        else:
            print(r.status_code,'网络代码',title,'url',url)
            # f.write(r.content)

    def webdownload(self,url):
        r = requests.get(url,headers=self.headers)
        r.encoding = 'urf-8'
        soup = BeautifulSoup(r.text,'html.parser')
        title = soup.body.find("div",class_="wrap")

    def web2download(self,url):
        #这里已经是最后一级目录了 在这里我们会抓到所有集数
        r = requests.get(url=url,headers=self.headers)
        r.encoding = 'utf-8'
        # soup = BeautifulSoup(r.text,'html.parser')
        # pattern = r'http://d.gqyy8.com:8077/ne2/s([0-9]*).js\?(\d+)'
        pattern = r'http://d.gqyy8.com:8077/ne2/s(?P<meiyong>[0-9]*).js\?(?P<jsid>\d+)'
        # matchObj = re.finditer( pattern, r.text, re.M|re.I)
        matchObj = re.search( pattern, r.text, re.M|re.I)
        a = matchObj.groupdict()
        # print(soup)
        print(matchObj.groupdict())
        return a.get('jsid')

    def jsanalyze(self,id,number,title):
        file = './video/'+title
        #id是影片唯一识别码 number是我抓到的 分析构成太麻烦偷懒一下
        jsurl = self.js_url.format(id,int(number))
        r = requests.get(url=jsurl,headers=self.headers)
        # pattern = r'playarr_2[1] = "https://kol-fans.fp.ps.netease.com/file/61588a3662b7347f8f8cc13dsCg39ir903,yj,12";'
        print(r.text)
        pattern = r'playarr\[([0-9]*)\]="(.*?),(.*?),(.*?)";'
        matchObj = re.findall(pattern,r.text,re.M|re.I)
        for i in matchObj:
            print(i[0],i[1])
            s = title + '第' + i[0] + '集'
            self.download(i[1],file,s)
            #我们在这里得到了 每一集所对应的网址 不过要对命名进行规范 所以要去读取一下 名字+集数+.mp4

    def main(self,s):
        #这个方法实现精准匹配下 抓取第一个符合的视频 并录入全集
        alist = self.post_search(s)#返回一个list 里面元素为字典 会有url thumb title time catid star lianzaijs beizhu alias_full area sort
        title = alist[0].get('title')
        if not os.path.exists('./video/'+title):
            os.mkdir('./video/'+title)
        aurl = alist[0].get('url')
        pattern = r'\/(\w*?)\/(\d*)\/'
        uid = re.findall(pattern,aurl,re.M|re.I)[0][1]
        url = self.index + aurl + '1' +'.html'
        print(uid,url,title)
        number = self.web2download(url)
        print("下载开始")
        self.jsanalyze(uid,number,title)
        print("下载完毕")

        return 



A = agefans()
# A.web2download('http://www.agefans.top/acg/26425/1.html')
# A.jsanalyze(65072,A.web2download('http://agefans.top/acg/65072/1.html'))
# A.web2download('http://agefans.top/acg/65072/1.html')
# A.post_search('鲁邦')
A.main('SSSS.DYNAZENON第一季')
# A.web2download('http://agefans.top/acg/66932/12.html')
# A.download('https://a13.fp.ps.netease.com/file/61a6ee763f043cbbd52dc909titKPBiP03','./video','鲁邦三世外传剧场版：次元大介的墓碑')

# url = 'http://d.gqyy8.com:8077/ne2/s26425.js?1638117843'
# r = requests.get(url)
# print(r.text)
