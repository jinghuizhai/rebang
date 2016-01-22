#!/usr/bin/env python
# -*- coding: utf-8 -*-
from controller import Controller

class Admin(Controller):
	def login(self,username,password):
		if username and password:
			return username+","+password
	