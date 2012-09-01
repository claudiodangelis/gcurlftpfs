from curlftpfs import curlftpfs
from sshfs import sshfs

class conn(object):

	__all__ = set()

	def __init__(self,username,password,server,port,mountpoint,protocol,name='Default'):
		
		self.username	= username
		self.password	= password
		self.server		= server
		self.port		= port
		self.mountpoint	= mountpoint
		self.protocol	= protocol
		self.name		= name
		
		if self.name == 'Default':
			self.name = self.server

		self.__class__.__all__.add(self)
		
	def mount(self):
		if self.protocol=='ftp':
			curlftpfs().mount(self)

		elif self.protocol == 'ssh':
			sshfs().mount(self)

	def unmount(self):
		if self.protocol == 'ftp':
			curlftpfs().unmount(self)
			
		elif self.protocol == 'ssh':
			sshfs().unmount(self)

	def remove(self):
		#	disconnect &
		#	remove from list [ self.__all__ ]
		return 0

	def __str__(self):
		return 'Connection: '+self.server
