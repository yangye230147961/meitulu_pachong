# -*- coding: utf-8 -*-
import requests
import re
import os

def url_ls(url):
    #获取页面所有套图链接
    html=requests.get(url)
    html.encoding=html.apparent_encoding
    url_ls=re.findall("https\:\/\/m\.meitulu\.com\/item\/\w+",html.text)
    return url_ls


def tup(url):
    #获取图片链接及套图名
    url_ls=[]
    num=1
    name=""
    while True:
        if num==1:
            url1=url+".html"
            num+=1
            print(name)
        else:
            url1=url+"_{}.html".format(num)
            num+=1
        print(url1)
        a=requests.get(url1)
        if a.status_code==404:
            break
        a.encoding=a.apparent_encoding
        my_url=re.findall("https\:\/\/mtl\.ttsqgs\.com\/images\/img\/\w+\/\w+\.jpg",a.text)
        if name=="":
            na=re.findall("\<h1\>[\w\W]+\<\/h1\>",a.text)
            nam=re.sub("\<h1\>","",na[0])
            name=re.sub("\<\/h1\>","",nam)
            print(name)
        for i in my_url:
            if "/0.jpg" not in i:
                url_ls.append(i)
    return url_ls,name

def w(url,name,num):
    headers={
'Host':'mtl.ttsqgs.com',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Linux; Android 7.1.2; M6 Note) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.105 Mobile Safari/537.36',
'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
'Referer':'https://m.meitulu.com/item/1.html',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9'
}
    
    print(name)
    print("正在下载{}".format(name))
    img=requests.get(url,headers=headers)
    os.system("clear")
    imga=img.content
    with open("./{}/{}.jpg".format(name,num),"wb") as f:
        print("正在写入{}".format(num))
        f.write(imga)
        f.close()
    
url=input("url")
urllist=url_ls(url)
for i in set(urllist):
    tup_ls,name=tup(i)
    p_ls=os.listdir()
    if name in p_ls:
        print("跳过")
    else:
        name=re.sub('[\/:*?"<>|]',"_",name)
        os.makedirs("./{}".format(name))
        n=0
        for j in tup_ls:
            n+=1
            num='{:0>4}'.format(n)
            w(j,name,num)

    