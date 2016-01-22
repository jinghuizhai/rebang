#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,copy,re,os
sys.path.insert(0,'..')
from engine.mysqlpy import Zsql

class Model(object):
	def __init__(self,**kw):
		self.__class__.__table__ = self.__table__
		if kw:
			for k,v in kw.items():
				setattr(self,k,v)

	def __str__(self):
		_str = list()
		for k,v in self.__dict__.items():
			_str.append(k+"=>"+str(v))
		return ','.join(_str)

	def _clear(self):
		self.__class__._where = None
		self.__class__._limit = None

	def dict2obj(self,args):
		ret = []
		that = copy.deepcopy(self)

		for key,value in that.__mapping__.items():
			setattr(that,key,None)

		if not isinstance(args,list) and not isinstance(args,tuple):
			args = tuple(args)
		for arg in args:
			clone = copy.deepcopy(that)
			for k,v in arg.items():
				setattr(clone,self.getkey(self.__mapping__,k),v)
			ret.append(clone)
		return ret

	def getkey(self,kw,value):
		"""
		根据dict的value返回对应的key
		"""
		for k,v in kw.items():
			if v == value:
				return k

	def save(self,**kw):
		"""
		初始化后，又传进参数，则初始化时部分参数会被覆盖，以新传入参数为准
		最后返回最后插入id，注意多线程
		"""
		if kw:
			for k,v in kw.items():
				setattr(self,k,v)
		columns = []
		values = []
		for k in self.__dict__:
			if self.__dict__[k] is not None:
				columns.append(self.__mapping__.get(k))
				values.append(self.__dict__[k])
		db = Zsql.get_instance()
		sql = 'insert into `%s`(%s) ' % (self.__class__.__table__,','.join(columns))
		sql = sql+'values('+','.join(['%s' for x in range(len(values))])+')'
		db.execute(sql,tuple(values))
		db.close()
		return db.lastid

	def find(self,*args):
		_args = []
		where_args = []
		for v in args:
			value = self.__mapping__.get(v)
			_args.append(value)
		if _args:
			_args = ','.join(map(str,_args))
		else:
			_args = " * "
		sql = 'select %s from `%s` ' % (_args,self.__class__.__table__)
		if getattr(self.__class__,'_where',None):
			_where = []
			for k,v in self.__class__._where.items():
				_where.append(k+"=%s")
				where_args.append(v)
			sql = sql + "where "+' and '.join(_where)
		if getattr(self.__class__,'_limit',None):
			sql = sql + ' limit %s' % self.__class__._limit
		db = Zsql.get_instance()
		db.execute(sql,tuple(where_args))
		result = db.fetchall()
		db.close()
		self._clear()
		return self.dict2obj(result)

	def findone(self,*args):
		_args = []
		where_args = []
		for v in args:
			value = self.__mapping__.get(v)
			_args.append(value)
		if _args:
			_args = ','.join(map(str,_args))
		else:
			_args = " * "
		sql = 'select %s from `%s` ' % (_args,self.__class__.__table__)
		if getattr(self.__class__,'_where',None):
			_where = []
			for k,v in self.__class__._where.items():
				_where.append(k+"=%s")
				where_args.append(v)
			sql = sql + "where "+' and '.join(_where)
		sql = sql+" limit 1"
		db = Zsql.get_instance()
		db.execute(sql,tuple(where_args))
		result = db.fetchone()
		db.close()
		self._clear()
		if result:
			return self.dict2obj([result])[0]
		else:
			return {}

	def where(self,**kw):
		_kw = dict()
		for k,v in kw.items():
			column = self.__mapping__.get(k)
			_kw[column] = str(v)
		self.__class__._where = _kw
		return self

	def limit(self,*limit):
		_limit = ''
		if limit:
			if len(limit) > 2:
				raise BaseException('limit length can not beyong 2')
			else:
				limit = map(int,limit)
				_limit = ",".join(map(str,limit))
		self.__class__._limit = _limit
		return self

	def update(self,**kw):
		"""
		在实例化对象后，可以直接调用此方法，将会把实例保存到数据库中
		所以调用此方法，不必传入kw参数
		传入kw参数，默认将参数保存到数据库中，实例化的参数部分失效或被覆盖
		比如:
			User(name='Tom').where(id=1).update()
			这时，id为1的对象名字将会变成Tom
		如果这样调用：
			User(name="Tom").where(id=1).update(name="Jack")
			Jack将会保存到数据库中，而不是Tom
		所以：
		kw会覆盖原来的对象
		最后返回影响行数
		"""
		if kw:
			for k,v in kw.items():
				setattr(self,k,v)
		columns = []
		values = []
		for k in self.__dict__:
			if self.__dict__[k] is not None:#k != id是根据系统的情况，id通常是主键，如果不是，应该去掉k!='id'
				columns.append(self.__mapping__.get(k))
				values.append(self.__dict__[k])
		column_str = list()
		for key in columns:
			column_str.append(key+"=%s")
		sql = 'update `%s` set %s' % (self.__class__.__table__,",".join([x+"=%s" for x in columns]))
		if getattr(self.__class__,'_where',None):
			sql = sql+" where %s" % (','.join([x+"=%s" for x in self.__class__._where]))
			[values.append(x) for x in self.__class__._where.values()]
		db = Zsql.get_instance()
		db.execute(sql,tuple(values))
		db.close()
		self._clear()
		return db.rowcount

	def delete(self,**kw):
		"""
		调用where方法时kw参数可以为空,比如obj.where(id=1).delete()
		不调用where方法时，kw参数不能为空，比如obj.delete()，这会抛出异常，正确的方法是obj.delete(id=1)
		如果where和delete方法的参数都不为空，则where方法的参数会覆盖delete的参数
		最后返回影响行数
		"""
		if getattr(self.__class__,'_where',None):
			kw = self.__class__._where
		else:
			if kw:
				_kw = dict()
				for k,v in kw.items():
					_kw[self.__mapping__[k]] = v
				kw = _kw
			else:
				raise KeyError('delete need 1 arguments!')
		sql = 'delete from %s where %s' % (self.__class__.__table__,",".join([x+"=%s" for x in kw.keys()]))
		db = Zsql.get_instance()
		db.execute(sql,tuple(kw.values()))
		db.close()
		self._clear()
		return db.rowcount


	def raw_sql(self,sql,args=[]):
		"""
		原生的sql语句执行,需要先实例化
		查询的数据在__mapping__的范围内则返回对象
		否则返回dict
		"""
		db = Zsql.get_instance()
		db.execute(sql,tuple(args))
		db.close()
		if re.search('^select',sql):
			result = db.fetchall()
			if result:
				data = result[0]
				if len(set(self.__mapping__.values()) & set(data.keys())) == len(data):
					return self.dict2obj(result)
				else:
					return result
			else:
				return {}
		elif re.search('^delete|^update|^insert',sql):
			return db.rowcount
		else:
			return {}
	
	@staticmethod
	def raw(sql,args=[]):
		"""
		静态方法，直接执行sql语句，不能转化为对象
		"""
		db = Zsql.get_instance()
		db.execute(sql,tuple(args))
		db.close()
		if re.search('^select',sql):
			return db.fetchall()
		elif re.search('^delete|^update|^insert',sql):
			return db.rowcount
		else:
			return {}

# class Test(Model):
# 	__table__ = 'test'
# 	__mapping__ = {
# 		'id':'test_id',
# 		'name':'name'
# 	}

# test = Test()
# print test.where(id=1).findone()
