from bs4 import BeautifulSoup
import urllib
from selenium import webdriver
import time
import os
import re
import requests

class Taolvlang(object):
    def __init__(self,driver,homePage,outputDir):
        self.driver = driver
        self.homePage = homePage
        self.outputDir = outputDir

    def get_detail_imgs(self,detail_url,dir_name):
        num = 0    #计数器，用于统计页面上的图片，作为图片名字
        self.driver.get(detail_url)  #访问个人主页
        js="var q=document.documentElement.scrollTop=10000"
        self.driver.execute_script(js)    #执行JS脚本，这个脚本主要是滚动页面到最下面，
        #因为有些网页是动态加载的，用户滑动到哪里加载到哪里
        bs = BeautifulSoup(driver.page_source,"html5lib")   #使用BeautifulSoup解析网页源码，使用的是html5lib,如果不安装这个库，会报错
        allImage = bs.findAll("img",{"src":re.compile("^\/\/img\.alicdn\.com\/imgextra\/.*.jpg$")}) #使用正则表达式匹配所有图片 
        for image in allImage:
            img_url = image["src"]    #获取图片的src
            if not img_url.startswith("http:"): 
                img_url = "http:"+img_url    #给图片地址加上http：
            num = num +1    #计数器+1
            r = requests.get(img_url)   #使用requests获取图片
            if not os.path.exists("%s/%d.jpg"%(dir_name,num)):    #判断是否已经存在这个文件了
                with open("%s/%d.jpg"%(dir_name,num),"wb") as pic:
                    pic.write(r.content)    #不存在的话就保存到文件中

    def get_all_data(self):  
        self.driver.get(homePage)   #访问主页
        js="var q=document.documentElement.scrollTop=10000"
        self.driver.execute_script(js)
        time.sleep(3)    #等待网页加载完成
        self.driver.get_screenshot_as_file("1.jpg")    #保存网页截图
        bs = BeautifulSoup(self.driver.page_source,"html5lib")    #使用BeautifulSoup解析网页源码，使用的是html5lib,如果不安装这个库，会报错
        allItem = bs.findAll(class_="item")   #找到所有的项，是class 为item的
        for item in allItem:
            detail_url = item.find(class_="item-link")["href"]  #获取个人主页连接
            header_img_url = item.find("img")["src"]   #获取封面图片链接
            dir_name = outputDir+"%s_%s"%(item.find(class_="name").get_text(),item.find(class_="city").get_text())   #获取名字和城市名组成文件夹名字
            if not os.path.exists(dir_name):   #如果文件夹不存在新建
                os.makedirs(dir_name)
            if not detail_url.startswith("http:"):
                detail_url = "http:"+detail_url
            if not header_img_url.startswith("http:"):
                header_img_url = "http:"+header_img_url
            print("detail_url=%s"%detail_url)
            print("header_img_url=%s"%header_img_url)
            #将头像存入目录
            if not os.path.exists(outputDir+"%s/0.jpg"%dir_name):
                urllib.request.urlretrieve(header_img_url,outputDir+"%s/0.jpg"%dir_name)
            #获取详细帖子中的照片
            self.get_detail_imgs(detail_url,dir_name)

    
#本地浏览器路径        
browserPath = "phantomjs.exe"
#主页路径
homePage = 'https://mm.taobao.com/search_tstar_model.htm?'
#输出目录
outputDir = "/photos/"   
driver = webdriver.PhantomJS(executable_path = browserPath)
#实例化类，执行获取数据
taoObj = Taolvlang(driver,homePage,outputDir)
taoObj.get_all_data()




        
    



























    
    
    

