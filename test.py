#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.model import Model
import sys,re,threading
# from time import *
import time

class Weixin(Model):

	__mapping__ = {
		'id':'weixin_id',
		'weixinnum':'weixinnum_id',
		'name':'name',
		'intro':'intro',
		'link':'link',
		'qrcode':'qrcode',
		'img':'head_img',
		'date':'date',
	}

def test():
	return 1

print test()
# weixin = Weixin(
# 	weixinnum='abc',
# 	name="python",
# 	intro="the best python 平台",
# 	link="http://weixin.sogou.com/python",
# 	qrcode="http://weixin.sogou.com/python/fkldsj.png",
# 	img="http://weixin.sogou.com/python/fklds.jpg",
# 	date="2015-01-02"
# )


now = time.time()
weixin = Weixin()

# for x in range(10000):
# 	weixin.save(weixinnum='python',name='python world',intro="最好的python号",link="haha",qrcode='heihei',img='hh',date='2015-02-15')

# print time.time()-now
# def insert():
# 	for i in range(10):
# 		weixin = Weixin()
# 		weixin.save(weixinnum='python',name='python world',intro="最好的python号",link="haha",qrcode='heihei',img='hh',date='2015-02-15')



# threads = []
# files = range(90)

# for i in files:
# 	t = threading.Thread(target=insert)
# 	threads.append(t)

# if __name__ == '__main__':
# 	for i in files:
# 		threads[i].start()

# 	for i in files:
# 		threads[i].join()

# 	print 'total time:%s' % str(time.time()-now)