#python download_nips.py --save_root paper --year 2018 --num_works 16

import requests,re,os,json
from pyquery import PyQuery as pq
from lxml import etree
import time
import sys
import argparse
from selenium import webdriver
from multiprocessing.pool import Pool

def gethtml(url):
    brower = webdriver.Chrome()
    brower.get(url)
    html = brower.page_source
    return html


# for i in range(5):
def GetPdf(year,root_path,num_works):

    url = 'https://papers.nips.cc/paper_files/paper/'+str(year)
    
    # html=gethtml(url)
    send_headers = {
        "User-Agent": "Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en,zh-Cn;q=0.9,zh;q=0.8,en-US;q=0.7"}
    print(1)
    html = requests.get(url, headers=send_headers)
    print(2)
    html=etree.HTML(str(html))
    PaperData = html.xpath('/html/body/div/div/ul/li/a/@href')
    base_url='https://papers.nips.cc//'
    PaperName = html.xpath('/html/body/div/div/ul/li/a/text()')

    print(len(PaperName))
    l = len(PaperName)+1
    g = len(PaperName)
    # NewUrl = [base_url + x for x in PaperData[1:]]
    # indexs=[0 for i in range(l)]
    
    # for i in range(l):
    #     html1=gethtml(NewUrl[i])
    #     html=etree.HTML(html1)
    #     indexs[i]=html.xpath('/html/body/div/div/div/a[3]/@href')#年份不同这里需要修改
    #     with open(UrlID,'wb') as f:
    #         print('正在抓取：'+PaperName)
    #         f.write(indexs[i])
    # NewIndexs = [base_url + x for x in indexs[1:]]

    # pool = Pool(processes=num_works)
    # pool.map(writepdf,zip(NewIndexs,PaperName, [root_path]*g))
    pool = Pool(processes=num_works)
    pool.map(writepdf,zip(PaperData, [root_path]*g))
    

def writepdf(info):
    PaperData, root_path = info
    base_url='https://papers.nips.cc//'
    # title = title.strip('\n')
    root_path = os.path.join(root_path,PaperData.split('/')[-3])
    if not os.path.exists(root_path):os.makedirs(root_path,exist_ok=True)
  
    NewUrl = base_url + str(PaperData)
    # print("NewUrl is :" ,NewUrl)
    # html1=gethtml(NewUrl)
    send_headers = {
        "User-Agent": "Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en,zh-Cn;q=0.9,zh;q=0.8,en-US;q=0.7"}
    html1 = requests.get(NewUrl, headers=send_headers)
    html=etree.HTML(html1)
    index = html.xpath('/html/body/div/div/div/a[2]/@href')#年份不同这里需要修改2017-2018是 a[3] 2019 是 a[5]
    title = html.xpath('/html/body/div/div/h4[1]/text()')
    title = str(title).replace(']','').replace('[','').replace('\'','')
    index = str(index).replace(']','').replace('[','').replace('\'','')
    url = base_url + index
    print("url:", url)
    send_headers = {
        "User-Agent": "Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en,zh-Cn;q=0.9,zh;q=0.8,en-US;q=0.7"}

    # print(url, title, root_path)
    response=requests.get(url,headers=send_headers)
    PDF_path=os.path.join(root_path,'{0}.{1}'.format(title.replace(':','').replace('?','').replace('/',' '),'pdf'))
    print(PDF_path)
    if not os.path.exists(PDF_path):
        os.makedirs(PDF_path)
        with open(PDF_path,'wb') as f:
            print('正在抓取：'+title)
            f.write(response.content)

    else:
        print('已下载: '+title)




if __name__=='__main__':

    parser = argparse.ArgumentParser(description="download ECCV paper")
    parser.add_argument("--save_root",type= str,  help="path to save paper")
    parser.add_argument("--year",type= str, help="download paper url ")
    parser.add_argument("--num_works",type=int,default=16,help="pool number of multiprocessing ")
    args = parser.parse_args()
    year = args.year
    save_root = args.save_root
    num_works = args.num_works

    

    # folder = url.split('/')[-1]
    root_path = save_root #os.path.join(save_root, folder)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    
    GetPdf(year,root_path,num_works)