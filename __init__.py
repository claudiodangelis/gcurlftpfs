import sys,os
from conn import conn

version	= '0.3.1'
testing	= True
debug	= True

if testing:
	a = conn('morph','mypass','192.168.0.9','22','/mnt/morpheus','ftp')

	print a
	a.mount()
