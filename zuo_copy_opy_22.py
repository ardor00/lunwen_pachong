# python download_nips.py --save_root paper --year 2018 --num_works 16
import random
import shutil

import requests, re, os, json
from pyquery import PyQuery as pq
from lxml import etree
import time
import sys
import argparse
from selenium import webdriver
from multiprocessing.pool import Pool

from selenium.webdriver.support.wait import WebDriverWait


def gethtml(url):
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ['enable-automation'])
    option.add_argument("headless")
    option.add_experimental_option('prefs', {
        "download.default_directory": "paper\\2019\\test",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # 这句配置很重要
    }
                                   )
    brower = webdriver.Chrome(options = option)
    brower.get(url)
    html = brower.page_source
    brower.close()
    return html


# for i in range(5):
def GetPdf(year, root_path, num_works):
    url = 'https://papers.nips.cc/paper_files/paper/' + str(year)
    root_path = os.path.join(root_path, year)
    if not os.path.exists(root_path): os.makedirs(root_path, exist_ok=True)
    download_dir = "paper\\2019\\test"
    if not os.path.exists(download_dir): os.makedirs(download_dir, exist_ok=True)
    html = gethtml(url)
    # send_headers = {
    #     "User-Agent": "Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    #     "Connection": "keep-alive",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #     "Accept-Language": "en,zh-Cn;q=0.9,zh;q=0.8,en-US;q=0.7"}
    # print(1)
    # html = requests.get(url, headers=send_headers)
    # html = requests.get(html)
    # print(2)
    html = etree.HTML(html)
    PaperData = html.xpath('/html/body/div/div/ul/li/a/@href')
    base_url = 'https://papers.nips.cc//'
    PaperName = html.xpath('/html/body/div/div/ul/li/a/text()')
    
    print(len(PaperData))
    l = len(PaperName) + 1
    g = len(PaperData)
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
    pool.map(writepdf, zip(PaperData, [root_path] * g))
    pool.close()
    pool.join()
    # for i in range(2125,l):
def writepdf(info):
        PaperData,root_path = info
        base_url = 'https://papers.nips.cc//'
        download_dir = "paper\\2019\\test"
        # title = title.strip('\n')


        NewUrl = base_url + str(PaperData)
        print("NewUrl is :", NewUrl)
        html1 = gethtml(NewUrl)
        # send_headers = {
        #     "User-Agent": "Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        #     "Connection": "keep-alive",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        #     "Accept-Language": "en,zh-Cn;q=0.9,zh;q=0.8,en-US;q=0.7"}
        # html1 = requests.get(NewUrl, headers=send_headers)
        html = etree.HTML(html1)
        index = html.xpath('/html/body/div/div/div/a[contains(@href,"Paper.pdf")]/@href')  # 年份不同这里需要修改2017-2018是 a[3] 2019 是 a[5]
        title = html.xpath('/html/body/div/div/h4[1]/text()')
        title = str(title).replace(']', '').replace('[', '').replace('\'', '')

        index = str(index).replace(']', '').replace('[', '').replace('\'', '')
        ll = len(index)
        time.sleep(1)

        url = base_url + index

        if len(url) < ll:
            url = base_url + index
        if url[-4:-1] != '.pdf':
            url = base_url + index
            print("url is :",url)
        # send_headers = {
        #     "User-Agent": "Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        #     "Connection": "keep-alive",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        #     "Accept-Language": "en,zh-Cn;q=0.9,zh;q=0.8,en-US;q=0.7"}
        # print(i)
        print(url, title, root_path)
        option = webdriver.ChromeOptions()

        option.add_experimental_option("excludeSwitches", ['enable-automation'])

        option.add_experimental_option('prefs', {
            "download.default_directory": "paper\\2019\\test",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True  # 这句配置很重要
        })
        driver = webdriver.Chrome(options=option)
        try:
            now_files = os.listdir(root_path)
            # driver.implicitly_wait(500)
            driver.get(url)
            paths = WebDriverWait(driver, 5000, 1).until(every_downloads_chrome)
            print(paths)
            # time.sleep(random.randint(1, 6))
            print("download!!!")
            driver.close()
            with open("22name.txt","a+") as f:
                title1 = title + "\n"
                f.write(title1)
            PDF_path = os.path.join(root_path)
            # for i in os.listdir(download_dir):
            #     if i not in now_files:
            #         time.sleep(random.randint(1,6))
            #         shutil.move(os.path.join(download_dir, i), os.path.join(PDF_path,i))
            #         break
        except:
            print("error")
            with open("error.txt","a+") as f:
                title1 = title + "\n"
                f.write(title1)
def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)

# waits for all the files to be completed and returns the paths






if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="download ECCV paper")
    parser.add_argument("--save_root", type=str, help="path to save paper")
    parser.add_argument("--year", type=str, help="download paper url ")
    parser.add_argument("--num_works", type=int, default=16, help="pool number of multiprocessing ")
    args = parser.parse_args()
    year = args.year
    save_root = args.save_root
    num_works = args.num_works

    # folder = url.split('/')[-1]
    root_path = save_root  # os.path.join(save_root, folder)
    if not os.path.exists(root_path):
        os.makedirs(root_path)

    GetPdf(year, root_path, num_works)
