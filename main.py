#coding=utf-8


import requests
from bs4 import BeautifulSoup 
import os
import threading
from time import sleep

def downloadimage(atlasdirname,count,suffix,url):
	res = requests.get(url)
	print('down {0} {1}{2}'.format(url,count,suffix))
	file = open('{0}{1}{2}'.format(atlasdirname,count,suffix),'wb')
	file.write(res.content)

def downpics(atlasdirname,url):
	#找到图片的地址，下载图片
	# p,n = os.path.splitext(url)
	# print(p)
	print(url)
	try:
		res = requests.get(url)
		res.encoding='GBK'
		soup = BeautifulSoup(res.text,'html.parser')
		totalpages = soup.select('.content .content-page .page-ch')[0].text.encode('GBK')
		count = int(totalpages[2:len(totalpages)-2])
		# 获得当前pic
		curimageurl = soup.select('.content  .content-pic img')[0]['src']
		p,n = os.path.splitext(curimageurl)
		for x in xrange(1,count+1):
			picurl = '{0}/{1}{2}'.format(os.path.dirname(p),x,n)
			print(picurl)
			downloadimage(atlasdirname,x,n,picurl)
	except Exception as e:
		pass
	

def downcurpage(dirname,upperurl,page = ''):
	#获取当前页图片列表
	print('dirname:{0},url:{1},page:{2}'.format(dirname,upperurl,page))
	res = requests.get(upperurl+page)
	res.encoding='GBK'
	soup = BeautifulSoup(res.text,'html.parser')
	imglist = soup.select('.main .public-box dd a')
	#获取当前页需要的a标签
	for a in imglist:
		if len(a.select('img'))>0:
			if a.select('img')[0].has_attr('alt'):
				title = a.select('img')[0]['alt'].encode('GBK')
				url = a['href']
				#建图片目录
				atlasdirname = '{0}{1}/'.format(dirname,title)
				if not os.path.exists(atlasdirname):
					os.mkdir(atlasdirname)
					#进入这个图集
				try:
					downpics(atlasdirname,url)
				except Exception as e:
					raise
				# sleep(5)
	#搞完这一页，去搞下一页
	navigation = soup.select('.main .page a')
	if len(navigation) > 0:
		for n in navigation:
			# 找到下一页
			if n.text.encode('utf-8') == "下一页":
				# 点击下一页
				if n.has_attr('href'):
					nexturl = n['href']
					downcurpage(dirname, upperurl , nexturl)

def getintonav(key,value):
	# 创建目录
	dirname = 'images/{0}/'.format(key)
	if not os.path.exists(dirname):
		os.mkdir(dirname) 
	downcurpage(dirname,value)
	

def getnavlist():
	res = requests.get('http://www.mm131.com/')
	res.encoding='gb2312'
	soup = BeautifulSoup(res.text,'html.parser')
	nav = soup.select('.nav')[0]
	alist = nav.select('a')
	diclist = {}
	for a in alist:
		if a.has_attr('href'):
			url = a['href']
			if url.startswith('http://www.mm131.com/') and len(url)>len('http://www.mm131.com/'):
				text = a.text.encode('gb2312')
				diclist[text] = url
	return diclist
		
		



# for i in range(1,65):
# 	downloadimage('http://img1.mm131.com/pic/2821/{0}.jpg'.format(i))
# 	sleep(1)
diclist = getnavlist()
for k,v in diclist.items():
	getintonav(k,v)