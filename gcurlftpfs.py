#! /usr/bin/env python

from gi.repository import Gtk
from gi.repository import Gdk
import subprocess, sys, os, threading, pprint
version='0.3.1'
debug=True

class about_window(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "About", parent, 0,
			(Gtk.STOCK_OK, Gtk.ResponseType.OK))

		self.set_default_size(450, 200)

		mainbox = self.get_content_area()

		title = Gtk.Label(justify=Gtk.Justification.CENTER)
		title.set_markup("<b>gcURLftpfs - "+version+"\n</b>")
		mainbox.add(title)

		desc = Gtk.Label(justify=Gtk.Justification.CENTER)
		desc.set_markup("Lightweight user interface and tools for curlftpfs program.\n")
		mainbox.add(desc)

		auth = Gtk.Label(justify=Gtk.Justification.LEFT)
		auth.set_markup("Claudio Dawson d\'Angelis (<a href='mailto:claudiodangelis@gmail.com'>claudiodangelis@gmail.com</a>)\nStefan Kent (<a href='mailto:skent@twosphere.com.au'>skent@twosphere.com.au</a>)\n\n<a href='http://www.claudiodangelis.it/projects/gcurlftpfs'>http://www.claudiodangelis.it/projects/gcurlftpfs</a>\n\n")
		mainbox.add(auth)

		self.show_all()


class main_window(Gtk.Window):

	def __init__(self):

		Gtk.Window.__init__(self, title="Grid Example")

		menu = Gtk.MenuBar()

		filemenu = Gtk.Menu()
		filem = Gtk.MenuItem("File")
		filem.set_submenu(filemenu)

		exit = Gtk.MenuItem("Exit")
		exit.connect("activate", Gtk.main_quit)
		filemenu.append(exit)
		menu.append(filem)

		helpmenu = Gtk.Menu()
		helpm = Gtk.MenuItem("Help")
		helpm.set_submenu(helpmenu)

		about = Gtk.MenuItem("About")
		about.connect("activate", self.show_about)
		helpmenu.append(about)
		menu.append(helpm)

		mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.add(mainbox)

		#Connections Component
		self.connectionbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		connectionframe = Gtk.Frame()
		spacerframe = Gtk.Frame()
		connectionframe.add(self.connectionbox)

		#Console Component
		consolebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

		consolelabel = Gtk.Label("Output:",justify=Gtk.Justification.LEFT)
		consolebox.pack_start(consolelabel,False,False,0)

		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_hexpand(False)
		scrolledwindow.set_vexpand(True)
		outputtextview = Gtk.TextView(editable=False)
		self.outputtext = outputtextview.get_buffer()
		scrolledwindow.add(outputtextview)
		consolebox.pack_start(scrolledwindow,True,True,0)

		#Build main form
		mainbox.pack_start(menu, False, False, 0)
		mainbox.pack_start(connectionframe, False, False, 0)
		mainbox.pack_start(spacerframe, True, True, 0)
		mainbox.pack_start(consolebox, True, True, 0)

	def show_about(self,widget):
		aboutdialog = about_window(self)
		aboutdialog.run()
		aboutdialog.destroy()

	def fc_forward(self):
		fc=fuse_connection()
		fc.pre_connect(self.hostname_entry.get(),self.username_entry.get(),self.password_entry.get(),self.port_entry.get(),self.mountpoint_entry.get())

	def fu_forward(self,umnt_hostname,umnt_mountpoint):
		self.umnt_hostname=umnt_hostname
		self.umnt_mountpoint=umnt_mountpoint
		fu=fuse_connection()
		fu.unmount(self.umnt_hostname,self.umnt_mountpoint)

	def feed_buffer_activity(self,buffered_text):
		self.outputtext.insert_at_cursor(buffered_text)

	def feed_ftp_buffer_activity(self,ftp_buffered_text):
		self.outputtext.insert_at_cursor(ftp_buffered_text)

	def open_folder(self,mountpoint):
		subprocess.Popen([open_cmd,mountpoint])

	def watch_mounted(self):
		self.mounted_hostname=[]
		self.mounted_mountpoint=[]
		proc = subprocess.Popen([mount_cmd],stdout=subprocess.PIPE)

		for child in self.connectionbox.get_children():
			child.destroy()

		#Collate data
		while True:
			procline = proc.stdout.readline()
			if procline != '':
				proclinetmp=procline.rstrip()
				if proclinetmp[0:9] == 'curlftpfs':
					procline_to_list=proclinetmp.split()

					tmp_mounted_hostname=procline_to_list[0]
					tmp_mounted_mountpoint=procline_to_list[2]

					if '@' in tmp_mounted_hostname:
						tmp_mounted_hostname=tmp_mounted_hostname.split('@')
						tmp_mounted_hostname=tmp_mounted_hostname[len(tmp_mounted_hostname)-1]

					tmp_mounted_hostname=tmp_mounted_hostname.split('/')
					tmp_mounted_hostname=tmp_mounted_hostname[len(tmp_mounted_hostname)-2]
					self.mounted_hostname.append(tmp_mounted_hostname)
					self.mounted_mountpoint.append(tmp_mounted_mountpoint)
			else:
				break

		#build GUI
		for i in range(len(self.mounted_hostname)):

			itemgrid = Gtk.Grid(column_spacing=20)

			label = Gtk.Label(justify=Gtk.Justification.LEFT)
			label.set_markup("<b>"+self.mounted_hostname[i]+"</b>")
			itemgrid.attach(label,1,1,3,1)

			mountlabel = Gtk.Label(justify=Gtk.Justification.LEFT)
			mountlabel.set_markup("<b>"+self.mounted_mountpoint[i]+"</b>")
			itemgrid.attach_next_to(mountlabel, label, Gtk.PositionType.RIGHT, 1, 1)


			openbutton = Gtk.Button("Open");
			openbutton.connect("clicked",lambda mnt_mountpoint=self.mounted_mountpoint[i] : self.open_folder(self.mounted_mountpoint[i]))
			itemgrid.attach(openbutton,1,2,1,1)

			umountbutton = Gtk.ToggleButton("Mounted");
			umountbutton.set_active(True)
			umountbutton.connect("clicked",lambda mnt_hostname=self.mounted_hostname[i],mnt_mountpoint=self.mounted_mountpoint[i]: self.fu_forward(mnt_hostname,mnt_mountpoint))
			itemgrid.attach_next_to(umountbutton, openbutton, Gtk.PositionType.RIGHT, 1, 1)

			removebutton = Gtk.Button("Remove");
			removebutton.connect("clicked",lambda mnt_mountpoint=self.mounted_mountpoint[i] : self.open_folder(self.mounted_mountpoint[i]))
			itemgrid.attach_next_to(removebutton, umountbutton, Gtk.PositionType.RIGHT, 1, 1)

			itemgrid.set_border_width(10)

			self.connectionbox.pack_start(itemgrid, True, True, 0)

		self.connectionbox.show_all()


class fuse_connection:
	def pre_connect(self,hostname,username,password,port,mountpoint):
		if hostname == "" or mountpoint == "":
			main_gui.feed_ftp_buffer_activity(app,'ERROR: hostname or mountpoint not given\n')
		else:
			if username=="":
				if password!="":
					main_gui.feed_ftp_buffer_activity(app,'WARNING: no username specified, password ignored\n')
				auth_data=""
			else:
				if password=="":
					auth_data=username
				else:
					auth_data=username+':'+password

			if port =="":
				port='21'


			auth_data='user=%s' % auth_data

			self.cmd_string=[]
			self.cmd_string.append(curlftpfs)
			self.cmd_string.append('-v')
			self.cmd_string.append('-o')
			self.cmd_string.append(auth_data)
			self.cmd_string.append(hostname+':'+port)
			self.cmd_string.append(mountpoint)
			self.connect(self.cmd_string)

	def connect(self,cmd_string):
		process = subprocess.Popen(self.cmd_string, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
		complete = False
		while True:
			output = process.stdout.read(1)
			if output == '' and process.poll() != None:
				break

			if output != '':
				sys.stdout.write(output)
				main_gui.feed_ftp_buffer_activity(app,output)
				sys.stdout.flush()

		main_gui.watch_mounted(app)
		if process.returncode ==0:
			main_gui.quick_connect_reset(app)

	def unmount(self,umnt_hostname,umnt_mountpoint):
		self.umnt_hostname=umnt_hostname
		self.umnt_mountpoint=umnt_mountpoint
		self.umnt_cmd_string=[unmount_cmd,unmount_flag,umnt_mountpoint]
		umnt_process = subprocess.Popen(self.umnt_cmd_string, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

		complete = False

		while True:
			umnt_output = umnt_process.stdout.read(1)
			if umnt_output == '' and umnt_process.poll() != None:
				break

			if umnt_output != '':
				sys.stdout.write(umnt_output)
				main_gui.feed_ftp_buffer_activity(umnt_output)
				sys.stdout.flush()

		main_gui.watch_mounted()

def check_dep(dependency):
	env_path=os.environ['PATH']
	env_path=env_path.split(':')
	for i in range(len(env_path)):
		if os.path.isfile(env_path[i]+'/'+dependency):
			return env_path[i]+'/'+dependency
	return 1

def fatal_error(err):
	print 'FATAL ERROR'
	if err==0:
		print 'Your operating system is not supported'
	elif err==1:
		print 'curlftpfs is required'
		print 'You can download it from:'
		print 'http://sourceforge.net/projects/curlftpfs/'
	elif err==2:
		print 'fusermount is required'
		print 'You can download them from'
		print 'http://sourceforge.net/projects/fuse/'

	print 'INFO: http://wwww.claudiodangelis.it/projects/gcurlftpfs'


#Create environment
OS=os.uname()
if OS[0]=="Darwin":
	mount_cmd="/sbin/mount"
	unmount_cmd="/sbin/umount"
	unmount_flag=""
	open_cmd="/usr/bin/open"
elif OS[0]=="Linux":
	mount_cmd="/bin/mount"
	unmount_cmd=check_dep('fusermount')
	unmount_flag="-u"
	open_cmd="xdg-open"
elif OS[0]!="Linux" and OS[0]!="Darwin":
	OS[0]=0

curlftpfs=check_dep('curlftpfs')

#Start application
win = main_window()
win.connect("delete-event", Gtk.main_quit)
win.set_title("gcURLftpfs")
win.set_default_size(750, 550)
win.show_all()

main_gui = win
app = win

win.watch_mounted()


Gtk.main()
