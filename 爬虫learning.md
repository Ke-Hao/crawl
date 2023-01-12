# Request

## 设置通用的URL模板

爬取多个页面内容：

~~~ python
url='https://www.baidu.com/%d/?s=1239'  #%d的位置为页码数
for pageNum in range (1,36):
    new_url = format(url%pageNum)
~~~

## bs4使用

### 对象实例化

1. 加载本地html文档：

   ~~~ python
   from bs4 import BeautifulSoup
   fp=open('path','r',encoding='utf-8')
   soup=BeautifulSoup(fp,'lxml') #固定使用lxml解析
   ~~~

2. 网页获取：

   ~~~ python
   page=response.text
   soup=BeautifulSoup(page,'lxml') #同样使用lxml解析
   ~~~

### 对象的函数

1. soup.tagName：会返回html中第一次出现的该标签

2. soup.find() : 若函数中填tagName，等同于1

   soup.find('tagName',class='') : 属性定位，定位到特定属性的tag

3. soup.find_all() : 符合要求的所有标签，返回形式为列表

4. soup.select() : 输入某种选择器，返回形式为列表

   层级选择 用 > 表示层级 （表示class选择器时需要加 . )

获取文本：

5. text / string / get_text() 函数：

   text / get_text() : 获得该标签内所有文本

   string：仅可以获取直系文本

获取标签中的属性：

6. soup.a['href'] : a 为上述函数之一

## xpath 解析数据

实例化对象：

~~~python
tree = etree.parse()
~~~

xpath表达式：

~~~ python
r = tree.xpath('/html/body/div') # /表示的是一个层级
r = tree.xpath('/html//div') # //表示多个层级 可从任意位置开始定位
r = tree.xpath('//div[@class="song"]') #属性定位
r = tree.xpath('//div[@class="song"]/p[3]') #索引定位 从1开始
~~~

取文本：

~~~ python
r = tree.xpath('//div[@class="song"]/p[3]/text()')[0]
# text()为取直系文本，取在列表中，需要加[0]取出内容
//text() #取出该标签中所有文本
~~~

取属性：

~~~ python
/@src  #格式为/@属性名称
~~~

## 对乱码的解决：

~~~ python
response=requests.get()
response.encoding='utf-8'
page_text=response.text
~~~

~~~ python
response.encoding=response.apparent_encoding
~~~

## 代理IP

1. 快代理
2. 西祠代理
3. www.goubanjia.com

## 异步爬虫

### 线程池(适当使用)

~~~python
from multiprocessing.dummy import Pool
## 需要实例化一个线程池对象
pool = Pool(4)
## map为异步的一种方法 将列表中每个元素传给函数
pool.map(function,list)

~~~

### 单线程+异步协程

1. event_loop：事件循环 相当于无限循环 满足某个条件 函数会循环执行
2. coroutine：协程对象 注册到事件循环中 使用async关键字定义一个方法 在调用时不会立即执行 而是返回一个协程对象
3. task：任务 对协程对象的封装 包含任务的各个状态
4. async：定义一个协程
5. await：挂起阻塞方法的执行

~~~ python
import asyncio #提供async和await关键字
# 1.async修饰的函数，调用后返回一个协程对象
async def request(url) 
c=request(url) # c为协程对象
# 2.创建一个事件循环对象
loop = asyncio.get_event_loop()
# 3.将协程对象注册到loop中，然后启动loop
loop.run_until_complete(c) 
~~~

task的使用：

~~~python
loop = asyncio.get_event_loop()
#基于loop创建一个task对象
task=loop.create_task(c)
loop.run_until_complete(task)
~~~

future的使用：

~~~python
task=asyncio.ensure_future(c) #协程对象注册
loop.run_until_complete(task)
~~~

绑定回调：

~~~ python
loop = asyncio.get_event_loop()
task=asyncio.ensure_future(c)
#将回调函数绑定到任务对象
task.add_done_callback(callback_function)
loop.run_until_complete(task)
~~~

多任务协程最终代码：

~~~python
urls=[] #列表中存放多个网址
tasks=[] #列表中存放多个任务对象
for url in urls:
    c=request(url) #request为async关键字修饰 返回协程对象
    task= asyncio.ensure_future(c)
    tasks.append(task)
    
loop =asyncio.get_event_loop() #事件循环对象
loop.run_until_complete(asyncio.wait(tasks)) #需要封装到wait
~~~

在异步中遇到阻塞必须手动挂起：

~~~ python
await asyncio.sleep(2)
# requests.get()基于同步实现 需使用aiohttp
import aiohttp
async def getpage(url):
    async with aiohttp.ClientSession() as session:
        async with await session.get(url) as response:
            #text()返回字符串
            #read()返回二进制
            page_text=await response.text() #!!!!
~~~

## selenium

### 动态加载的数据

在检查中ctrl+F搜索，通过请求的URL获取

### selenium优势

1. 获取动态加载数据
2. 模拟登录

### 驱动程序

1. webdriver_manager.chrome包

2. 下载路径：http://chromedriver.storage.googleapis.com/index.html

   需csdn查看对应浏览器版本

### 使用方法

~~~ python
from selenium import webdriver
#实例化一个浏览器对象 传入浏览器驱动
bro=webdriver.Chrome(executable_path='./chromedriver')

# 浏览器发请求
bro.get(url)

# 获取浏览器页面源码
page_text=bro.page_source

# 需要停留一段时间再关闭
# from time import sleep
sleep(5)
bro.quit()

# 标签定位
s=bro.find_element_by_id('q')
# 标签交互
s.send_keys('')
# 按钮点击
button.click()

# 滚轮拖动 (拖动一屏 水平,垂直)
# 执行一组js
bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')

# 回退(返回上一页面)/前进
bro.back() / bro.forward()

~~~

### iframe

嵌套子页面 若直接定位子页面中的标签则定位不到

~~~ python
# 切换浏览器标签定位的作用域	
bro.switch_to.frame('name') 

# 导入包
from selenium.webdriver import ActionChains
# 实例化动作链对象
action=ActionChains(bro)

# 点击长按指定标签
action.click_and_hold(div)
# 拖动
for i in range(5)
	# perform()立即执行动作链操作
	action.move_by_offset(17,0).perfprm()
    sleep(0.3)

~~~

### 无头浏览器

~~~ python
from selenium.webdriver.chrome.options import Options
# 不会弹出可视化界面
# phantomJs有同样效果
chrome_options=Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
bro=webdriver.Chrome(executable_path='',chrome_options=chrome_options)
~~~

### 实现规避检测

~~~ python
from selenium.webdriver import ChromeOptions

option=ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])
#driver=Chrome(options=option)
~~~

# scrapy

## 基本使用

~~~ python
# 创建工程：
scrapy startproject filename
# spiders子目录下创建爬虫文件(cd到工程文件夹中)：
scrapy genspider filename www.xxx.com
# 执行工程
scrapy crawl filename
# 不显示日志
--nolog
# allowed_domains为允许域名 限定start_urls中哪些url会发送请求 通常注释
# parse用于数据解析
~~~

## 数据解析

~~~ python
# 仍使用xpath 但返回为selector类型

# 使用extract()提取data中的文本
content=div.xpath('').extract()
# 对列表调用时：
content=''.join(content)
# extract_first()获取第一个元素的文本
~~~

## 持续化存储

### 基于终端指令

只可将parse返回值存储到本地 存储类型有限 

~~~python
scrapy crawl filename -o path
~~~

### 基于管道

编码流程：

	1. 数据解析
 	2. 在item类中定义相关属性
 	3. 将数据封装成item类型对象
 	4. item对象提交给管道
 	5. 管道类process_item中将接收的item中的数据持久化存储
 	6. 在配置文件中开启管道

~~~python
from proname.items import pronameItem
# 在parse中：
# 实例化item对象
item=pronameItem()
item['author']=author
item['content']=content
# 提交管道
yield item

# 在items中：
author=scrapy.Field()
content=scrapy.Field()

# 在pipelines中：
fp=None
# 重写父类的方法：只在开始爬虫时调用一次：
def open_spider(self,spider):
    print('开始爬虫')
  	self.fp=open('path','w',encoding='utf-8')
# 每接收一个item调用一次：
def process_item(self,item,spider):
    author=item['author']
    content=item['content']
    self.fp.write(author+content)
# 结束爬虫时调用：
def close_spider(self,spider):
	print('结束')
	self.fp.close()
~~~

## 配置文件

~~~ python
# 不遵守Robots协议
ROBOTSTXT_OBEY=False
# 显示错误日志
LOG_LEVEL='ERROR'
# 启用UA屏蔽
USER_AGENT=''
# 开启管道 取消ITEM_PIPELINES注释
# 图片存储位置：
IMAGES_STORE='./imgs'
~~~

## 全站爬取

~~~ python
# 通用url模板
url='...%d...'
page_num=2

# parse中
# 在正常数据处理后：
new_url=format(self.url%self.page_num)
self.page_num+=1
# 手动请求发送：callback回调函数专门用于数据解析
yield scrapy.Request(url=new_url,callback=self.parse)
~~~

## 深度爬取

需要在爬虫文件中新建数据解析函数

~~~python
yield scrapy.Request(url=new_url,callback=self.parse_detail，meta={'item':item})
# 接收参数
response.meta['item']
~~~

## 图片数据爬取

步骤：

> 数据解析（图片地址）
>
> 将存储地址的item提交到特定管道
>
> 自定义管道类：
>
> > get_media_request
> >
> > file_path
> >
> > item_completed
>
> 在配置文件中：
>
> > 指定图片存储位置
> >
> > 指定开启的管道类

~~~python
# 使用伪属性
src2

# pipelines中：
from scrapy.pipelines.images import ImagesPipeline
class imgsPipeLine(ImagesPipeline):
    # 请求
    def get_media_requests(self,item,info):
        yield scrapy.Request(item['src'])
    # 指定存储路径：
    def file_path(self,request,response=None,info=None):
        imgname=request.url.split('/')[-1]
        return imgname
    def item_completed(self,results,item,info):
    	return item
~~~


