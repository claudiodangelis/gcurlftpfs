class sshfs(object):

	def mount(self,conn):
		print 'Performing a sshfs connection:'
		print conn.username
		print conn.password
		print conn.server
		print conn.port
		print conn.mountpoint
		print conn.name

	def unmount(self,conn):
		print 'Unmounting:'
		print conn.username
		print conn.password
		print conn.server
		print conn.port
		print conn.mountpoint
		