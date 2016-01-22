#!/usr/bin/env python
# -*- coding: utf-8 -*-
from controller import Controller
from model.recommend import ModelRecommend
from model.weixin import ModelWeixin

class Recommend(Controller):
	def recommend(self,weixin,weixinnum_id):
		weixin = weixin.strip()
		weixinnum_id = weixinnum_id.strip()
		if len(weixin)>5 and len(weixinnum_id)>5:
			weixin = ModelWeixin()
			result = weixin.where(name=weixin).findone(*['name'])
			if result:
				return False,'公众号已经存在'
			else:
				recommend = ModelRecommend()
				# result = recommend.insert(name=weixin,weixin_en=weixinnum_id)
				result = True
				# print("weixin=%s,weixinnum_id=%s" % (weixin,weixinnum_id))
				if result:
					return True
				else:
					return False,'公众号存入失败'
		else:
			return False,'公众号或ID太短'