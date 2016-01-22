#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
from config import config
class Zsql():

	@classmethod
	def get_instance(self):# 类方法也需要传参
		Zsql._instance = Zsql(**config['db_config'])
		return Zsql._instance

	def __init__(self,**kw):
		config = {
          'user':kw.get('user','root'), 
          'password':kw.get('password',''), 
          'host':kw.get('host','localhost'), 
          'port':kw.get('port',3306),  
          'database':kw.get('database','test'),
          "cursorclass":pymysql.cursors.DictCursor
        }
		try:
			self.conn = pymysql.connect(**config)
			self.cursor = self.conn.cursor()
			self.autocommit(True)
		except BaseException as e:
			print 'init'
			raise e
		

	def execute(self,sql,data=()):
		# try:
		# 	self.cursor.execute(sql,data)
		# 	# cursor.lastrowid conn.insert_id()
		# 	self.lastid = self.cursor.lastrowid
		# 	self.rowcount = self.cursor.rowcount
		# except BaseException as e:
		# 	print 'execute'
		# 	raise e
		self.cursor.execute(sql,data)
		self.lastid = self.cursor.lastrowid
		self.rowcount = self.cursor.rowcount

	def close(self):
		self.conn.close()

	def executemany(self,sql,data=()):
		try:
			self.cursor.executemany(sql,data)
			self.lastid = self.cursor.lastrowid
			self.rowcount = self.cursor.rowcount
		except BaseException as e:
			# self.close()
			raise 'lianjie'

	def fetchone(self):
		return self.cursor.fetchone()

	def fetchall(self):
		return self.cursor.fetchall()

	def fetchmany(self,count):
		return self.cursor.fetchmany(count)

	def autocommit(self,auto=True):
		self.conn.autocommit(auto)

	def commit(self):
		self.conn.commit()

	def rollback(self):
		self.conn.rollback()


# db = Zsql(**config['db_config'])
# db.execute('insert into `test` set name = %s',('tyu'))
# db.close()
# print db.fetchall()
# print db.lastid
# print db.rowcount
