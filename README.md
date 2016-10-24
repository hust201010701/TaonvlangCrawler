# TaonvlangCrawler   Python3 实现淘女郎照片爬虫 （完整版教程）
----------

##一. 项目介绍
本项目通过Python 3实现一个爬取淘女郎网页上的美女的头像和详细介绍帖子中的所有图片并下载到本地来。

**Todo:**
1. 将图片自动上传到七牛等云存储空间中
2. 将图片的信息添加到在线数据库中


##二. 知识点

1. 使用Python 3编程
2. 使用BeautifulSoup解析html网页
3. 使用Selenium抓取动态网页
4. 下载文件的几种方式
5. 正则表达式的使用

##三. 项目效果

这是我们要爬取的目标页面：

淘女郎：[https://mm.taobao.com/search_tstar_model.htm](https://mm.taobao.com/search_tstar_model.htm)

**目标页面**
![](http://pic.sdodo.com/tool/picadjust/r.php?fu=../_tempf/1024/1477291730-55.jpg&fn=1477291730-55.jpg&type=jpg)

**爬取后的本地目录**
![](http://pic.sdodo.com/tool/picadjust/r.php?fu=../_tempf/1024/1477291921-20.jpg&fn=1477291921-20.jpg&type=jpg)
**每个目录中的图片**
![](http://pic.sdodo.com/tool/picadjust/r.php?fu=../_tempf/1024/1477292147-65.jpg&fn=1477292147-65.jpg&type=jpg)

##四. 项目实战

#4.1 安装需要使用的库
	
以下是本项目需要使用到的库文件：

	from bs4 import BeautifulSoup
	import urllib
	from selenium import webdriver
	import time
	import os
	import re
	import requests

需要安装的几个库是bs4，selenium,requests.安装方式是使用pip，分别运行下面的命令：

	pip install BeautifulSoup4
	pip install selenium
	pip install requests
	pip install html5lib

Selenium 是一个强大的网络数据采集工具，最初是为网站自动化测试而开发的。近几年，他还被广泛用于获取精确的网站快照，因为他们可以直接运行在浏览器上。Selenium 可以让浏览器自动加载页面，获取需要的数据，甚至页面截屏，或者判断网站上某些动作上是否发生。

Selenium 自己不带浏览器，它需要与第三方浏览器结合在一起使用。我们使用的是PhantomJS浏览器，这是一个无头的浏览器，PhantomJS 会把网站加载到内存并执行页面上的 JavaScript，但是不会向用户展示网页的图形化界面，可以用来处理 cookie、JavaScript 及 header 信息，以及任何你需要浏览器协助完成的事情。

可以去链接下载，也可以自行搜索下载：

链接：[http://pan.baidu.com/s/1eSLrpzs](http://pan.baidu.com/s/1eSLrpzs) 密码：vsq9

#4.2 项目目标

1. 抓取淘女郎页面中美女的封面，昵称和城市
2. 抓取个人主页中图片
3. 将每个美女的图片以文件夹的形式存储在文件夹中

#4.3 可行性分析

淘女郎首页上的源码信息是公开的，本次实验仅仅是用来技术实践，并不带盈利性目的，也不将图片用于其他商业环境，并不会产生商业上的产权纠纷，所以这个项目是可行的。

#4.4 流程说明

通过 Selenium Webdriver 获得目标页面源码，之后通过 BeautifulSoup 解析概源码，通过正则表达式提取出模特名字、所在城市、身高、体重，个人主页、封面图片地址等信息，根据模特名字和城市建立文件夹。

再次通过 Selenium Webdriver 获得模特个人主页的页面源码，之后通过 BeautifulSoup 解析源码，通过正则获得页面艺术照的URL地址信息。

最后通过 urllib 内置库，打开图片地址，通过二进制读写的方式获得模特艺术照，并将艺术照存在相应文件夹里面。

#4.5 网页源码分析

![](http://i.imgur.com/gtNM6Un.jpg)

图中的1,2,3,4分别代表该MM的个人介绍主页地址，封面图片地址，名字和城市，身高体重。第四个我们不使用，只需要获取前三个信息即可。进入个人主页，我们继续类似前面的审查元素，可以看到

	<img style="width: 630.0px;float: none;margin: 10.0px;height: 945.0px;" width="630" height="945" src="//img.alicdn.com/imgextra/i2/927018118/TB1vpJVNVXXXXXzaXXXXXXXXXXX_!!0-tstar.jpg">

里面的图片的标签都是img，而且图片的网址前面是一样的，因此可以使用正则表达式来匹配图片地址：

	^\/\/img\.alicdn\.com\/imgextra\/.*\.jpg$

这样可以过滤掉其他图片。

#4.6 程序实战

首先导入要使用的库

	from bs4 import BeautifulSoup
	import urllib
	from selenium import webdriver
	import time
	import os
	import re
	import requests

建一个类，叫做Taonvlang,里面有几个函数：

get_detail_imgs(self,detail_url,dir_name):  根据detail_url获取个人主页图片，并存到目录dir_name中

get_all_data(self): 获取主页的所有的美女封面和个人主页

__init__(self,driver,homePage,outputDir): 初始化函数，初始化类中变量

具体查看代码

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

##五.项目地址

[https://github.com/hust201010701/TaonvlangCrawler](https://github.com/hust201010701/TaonvlangCrawler)

欢迎大家Star.

 
    


