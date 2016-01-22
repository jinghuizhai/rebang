#! usr/bin/python
# -*- coding:utf-8 -*-

import requests
import re
from HTMLParser import HTMLParser
from pyquery import PyQuery as pq
import urllib
import time
import json
import  xml.dom.minidom
import sys

# reload(sys)
# sys.setdefaultencoding('gbk')


# reload(sys)
# sys.setdefaultencoding('utf-8')
# strs = '<![CDATA[Python开发者]]>'
# print re.search('<!\[CDATA\[(.*)\]\]>',strs).groups()[0]
# exit()

class GrabWinxin():

	def __init__(self):

		self.cookies = dict()
		self.host = 'http://weixin.sogou.com/weixin'

	def clear_html(self,html):
		'删除html标签'
		if html:
			return re.sub('<[^>]+>','',html)
		else:
			return ''

	def grab(self,url,params={}):

		'爬虫抓取内容'
		headers = {
			'Host':'weixin.sogou.com',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
			'Connection':'keep-alive',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Cache-Control':'max-age=0',
			'Accept-Language':'Accept-Language:zh-CN,zh;q=0.8'
		}
		proxies = {'http':'http://218.200.66.196:8080','https':'http://218.200.66.196:8080'}
		proxies = {}
		try:
			r = requests.get(url,headers=headers,proxies=proxies,params=params,cookies=self.cookies,timeout=1)
			if r.status_code == 200:
				response_cookies = dict()
				if r.cookies:
					print r.cookies
					for key,value in r.cookies.items():
						response_cookies[key] = value
					self.cookies = response_cookies
				return r.content
			else:
				return False
		except BaseException as e:
			print e
			return False#超时

	def get_weixin(self,name,weixin_id=''):

		"""抓取微信概要信息"""
		if name:
			params = ['type=1','query='+name,'ie=utf8']
			url = self.host+"?"+'&'.join(params)
			# url = urllib.quote(url)
			html = self.grab(url)
			if html:
				query = pq(html)
				div_class = query('.wx-rb')
				ret_list = []
				for key_class in div_class:
					w_id = pq(key_class)('h4').find('span').html()
					if weixin_id:
						if w_id != weixin_id:
							break
					href = pq(key_class).attr('href')
					if href:
						href = "http://weixin.sogou.com"+href
					img = pq(key_class)('.img-box').find('img').attr('src')					
					name = self.clear_html(pq(key_class)('h3').html())
					intro = self.clear_html(pq(key_class)('.sp-txt').html())
					qrcode = pq(pq(key_class)('.pos-ico').find('img')[1])('img').attr('src')
					if w_id:
						w_id = re.sub('[^\d_\w]','',w_id)
					ret_list.append({'href':href,'img':img,'name':name,'weixin_id':w_id,'intro':intro,'qrcode':qrcode})

				return ret_list
		else:
			return None

	def get_weixin_list(self,url=''):

		"""抓取微信内容"""
		url = 'http://weixin.sogou.com/gzh?openid=oIWsFt-RHrNpIeYgvcC-ouufPF3o&ext=JWYPUbr8sGo2-viZDZdHBByWo8ePKIagdPCPeQ1DhiLHuG2wvG1ZCYYQnI_nfN7Y'
		openid = re.search('openid=([^&]+)',url)
		ext = re.search('ext=([^&]+)',url)
		if openid:
			openid = openid.groups()[0]
		else:
			openid = ''
		if ext:
			ext = ext.groups()[0]
		else:
			ext = ''

		params = {
			'cb':'sogou.weixin.gzhcb',
			'openid':openid,
			'ext':ext,
			'page':1,
			't':int(time.time())
		}
		#先访问一次，获取cookies
		self.grab(url)
		time.sleep(3)
		content = self.grab("http://weixin.sogou.com/gzhjs",params)
		if content:
			try:
				m = re.search('([{][^{}]+[}])',content)
				obj = m.groups()[0]
				jsons = json.loads(obj)
				if int(jsons['totalPages']) > 0:
					items = jsons['items']
					for i in items:
						i = i.encode('utf-8')
						title = re.search('<title><!\[CDATA\[(.*)\]\]></title>',i).groups()[0]
						url = re.search('<url><!\[CDATA\[(.*)\]\]></url>',i).groups()[0]
						html = self.grab('http://weixin.sogou.com'+url)
						# print html
						break
				else:
					print 'no page any more'
			except BaseException as e:
				print 'error'
		else:
			print 'no json content data'

		
			
			


# print help(xml.dom.minidom)

weixin = GrabWinxin()
print weixin.get_weixin('python')
# weixin.get_weixin_list()
