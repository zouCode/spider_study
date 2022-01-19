# 爬取网页前四页的所有音乐下载
"""""
课后作业:
	熊猫办公网站音频数据获取4页
	网址:https://www.tukuppt.com/peiyue/
	保存音频数据	
请跳转至51行修改保存路径-_-||
"""""
from lxml import etree
import sys,os
from lxml.html import tostring
from contextlib import closing
import requests
def download_file(d_url,path,name,page):
    file_name = path+str(name)+".mp3"
    with closing(requests.get(d_url,stream=True))as r:
        chunk_size = 1024
        content_size = int(r.headers['content-length'])
        print('下载 page{}  {}.mp3 \n请等待...'.format(page,name))
        with open(file_name,'wb')as f:
            n = 1
            for chunk in r.iter_content(chunk_size=chunk_size):
                loaded = int(n*1024.0/content_size*100)
                f.write(chunk)
                s="\r%d%% %s"%(loaded,"#"*int(loaded/2))   #\r表示回车但是不换行，利用这个原理进行百分比的刷新
                sys.stdout.write(s)       #向标准输出终端写内容
                sys.stdout.flush()        #立即将缓存的内容刷新到标准输出
                n += 1
        print("\n")

url ="https://www.tukuppt.com/peiyue/"
for num in range(4):
    if num > 0:
        url ="https://www.tukuppt.com/peiyue/zonghe_0_0_0_0_0_0_{}.html".format(num+1)
    name_list = []
    link_list = []
    ht = requests.get(url=url)
    x_html = etree.HTML(ht.text) 
    # 提取名字
    names = x_html.xpath('//a[@class="title"]')
    for name in names:
        name = tostring(name,encoding='utf-8').decode('utf-8')
        name_list.append(name[61:-22])
        #print(name[61:-22])
    # 提取下载链接
    link = x_html.xpath('//source/@src')
    for lik in link:
        lik = "http:"+lik
        #print((lik))
        link_list.append(lik)
    file_path = "C:/Users/zouqi/Desktop/spider/music/{}/".format(num+1)   #请根据自己电脑修改此处路径
    if(os.path.exists(file_path)==False):
        os.mkdir(file_path)
    for i in range(len(name_list)):
        #print(name_list[i]+link_list[i])
        download_file(link_list[i],file_path,name_list[i],num+1)
print('所有页面的音乐已下载完成!')
