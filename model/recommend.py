#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model import Model
import time

class ModelRecommend(Model):
	__table__ = 'recommend'
	__mapping__ = {
		'id':'recommend_id',
		'weixin_en':'weixinnum_id',
		'name':'name',
		'date':'date',
		'states':'states'
	}

	def insert(self,**kwarg):
		return self.raw_sql('insert into `recommend`(weixinnum_id,name,date,states) values(%s,%s,%s,%s)',tuple([
			kwarg.get('weixin_en'),
			kwarg.get('name'),
			str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))),
			'0'
		]))

# mr = ModelRecommend()
# print mr.insert(weixin_en='python',name='python公众号')
