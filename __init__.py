import sys,os
from conn import conn

global testing

version	= '3.1'
testing	= True
debug	= True

if testing:
	a = conn('morph','mypass','192.168.0.9','22','/mnt/morpheus','ssh')

	print a
	a.mount()