#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,redirect,url_for
from controller.admin import Admin
from controller.recommend import Recommend

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('catalog/index.tpl')

@app.route('/recommend',methods=['GET','POST'])
def recommend():
	if request.method == 'GET':
		return render_template('catalog/recommend.tpl')
	else:
		recommend = Recommend()
		print request.form['weixin'],request.form['weixinnum_id']
		result = recommend.recommend(request.form['weixin'],request.form['weixinnum_id'])
		if isinstance(result,tuple):
			if result[0] is False:
				return result[1]
		else:
			return 'success'


@app.route('/admin/login',methods=['GET','POST'])
def admin():
	admin = Admin()
	if request.method == 'GET':
		return render_template('admin/login.tpl')
	else:
		return admin.login(request.form['username'],request.form['password'])



if __name__ == '__main__':
    app.run(debug=True)