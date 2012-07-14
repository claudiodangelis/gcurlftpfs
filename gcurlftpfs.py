#! /usr/bin/env python
from Tkinter import *
import tkFileDialog, subprocess, sys, os, threading
version='0.2.1'
debug=False
class about:
	def __init__(self,root):
		self.root=root
		self.main_about=Frame(root,pady=20,padx=20)
		self.main_about.grid()
		Label(self.main_about,text='gcurlftpfs - '+version+'\n',font="mono 14").grid()
		Label(self.main_about,text='Lightweight user interface and tools for curlftpfs program.\n').grid()
		Label(self.main_about,text="Original author: Claudio Dawson d\'Angelis (info@claudiodangelis.it)\n\nhttp://www.claudiodangelis.it/projects/gcurlftpfs\n\n").grid()	
		Button(self.main_about,text="OK",command=self.root.destroy,width=10,pady=-2,padx=-2).grid()

class main_gui:
	def __init__(self,root):
		root.protocol('WM_DELETE_WINDOW', lambda : root.destroy())
		self.mnt=StringVar()
		self.conta=0
		self.root=root
		self.main_frame=Frame(root,padx=5,pady=5)
		self.main_frame.grid()
		menubar = Menu(root)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Exit", command=root.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="About", command=self.pre_about)
		menubar.add_cascade(label="Help", menu=helpmenu)
		root.config(menu=menubar)
		self.left_frame=Frame(self.main_frame,relief=GROOVE,padx=10,pady=10,borderwidth=2)
		self.left_frame.grid(row=0,column=0,sticky=NW)
		Label(self.left_frame,text='Connect').grid()
		self.activity_frame=Frame(self.main_frame,relief=GROOVE)
		self.activity_frame.grid(pady=5,row=1,columnspan=999)
		Label(self.activity_frame,text='Console').grid(row=0,sticky=W)
		self.s = Scrollbar(self.activity_frame)
		self.buffer_activity = Text(self.activity_frame)
		self.buffer_activity.config(yscrollcommand=self.s.set,relief=SUNKEN,font='mono 9',height=10,width=100)
		self.buffer_activity.grid(row=1,column=0,sticky=EW)
		self.s.grid(sticky=NSEW,row=1,column=1)
		self.s.config(command=self.buffer_activity.yview)
		self.mounted_frame=Frame(self.main_frame,relief=GROOVE,padx=10,pady=10,borderwidth=2)
		self.mounted_frame.grid(row=0,column=1,sticky=E+W+N+S,columnspan=999)
		Label(self.mounted_frame,text='Mounted hosts').grid(row=0,column=0,sticky=W)
		Button(self.mounted_frame,text='Refresh',width=8,command=lambda : self.watch_mounted(),padx=-3,pady=-3).grid(row=1,sticky=W)
		self.mounted_entries_frame=Frame(self.mounted_frame)
		self.mounted_entries_frame.grid(sticky=E+W)
		Label(self.left_frame, text="Hostname").grid(row=1,column=0,sticky=E)
		self.hostname_entry=Entry(self.left_frame, width="25")
		self.hostname_entry.grid(row=1,column=1,sticky=W)
		self.hostname_entry.focus_set()
		Label(self.left_frame, text="Username").grid(row=2,column=0,sticky=E)
		self.username_entry=Entry(self.left_frame, width="25")
		self.username_entry.grid(row=2,column=1,sticky=W)
		Label(self.left_frame, text="Password").grid(row=3,column=0,sticky=E)
		self.password_entry=Entry(self.left_frame, width="25", show="*")
		self.password_entry.grid(row=3,column=1,sticky=W)
		Label(self.left_frame, text="Port (default: 21)").grid(row=4,column=0,sticky=E)
		self.port_entry=Entry(self.left_frame, width="3")
		self.port_entry.grid(row=4,column=1,sticky=W)
		Label(self.left_frame, text="Mountpoint").grid(row=5,column=0,sticky=E)
		Label(self.left_frame, text="(absolute path)").grid(row=6,column=0,sticky=E)
		
		self.mountpoint_entry=Entry(self.left_frame, width="18")
		self.mountpoint_entry.grid(row=5,column=1,sticky=W+E)
		
		Button(self.left_frame,text='...',pady=-3,command=self.choose_folder).grid(row=5,column=1,sticky=E)
		Button(self.left_frame,text="Connect",command=self.fc_forward,pady=-1).grid(row=7,column=0,sticky=E,pady=8)
		Button(self.left_frame,text="Reset",command=self.quick_connect_reset,pady=-1).grid(row=7,column=1,sticky=W,pady=8)

		self.watch_mounted()
			
	def pre_about(self):
			root_about=Tk()
			aboutme=about(root_about)
			root_about.wm_title("About")
			root_about.mainloop()
				
	def fc_forward(self):
		fc=fuse_connection()
		fc.pre_connect(self.hostname_entry.get(),self.username_entry.get(),self.password_entry.get(),self.port_entry.get(),self.mountpoint_entry.get())
		
	def fu_forward(self,umnt_hostname,umnt_mountpoint):
		self.umnt_hostname=umnt_hostname
		self.umnt_mountpoint=umnt_mountpoint
		fu=fuse_connection()
		fu.unmount(self.umnt_hostname,self.umnt_mountpoint)
	
	def watch_mounted(self):
			self.mounted_entries_frame.destroy()
			self.mounted_entries_frame=Frame(self.mounted_frame)
			self.mounted_entries_frame.grid()
			self.mounted_hostname=[]
			self.mounted_mountpoint=[]
			proc = subprocess.Popen([mount_cmd],stdout=subprocess.PIPE)
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
			
			for i in range(len(self.mounted_hostname)):							
				self.mef=Frame(self.mounted_entries_frame, relief=GROOVE, borderwidth=1)
				self.mef.grid(sticky=E+W,pady=4)
				Label(self.mef,text=self.mounted_hostname[i],font="mono 12").grid(padx=4,row=0,column=0,sticky=EW)
				Button(self.mef,text='Open',width=8,command=lambda mnt_mountpoint=self.mounted_mountpoint[i] : self.open_folder(mnt_mountpoint),padx=-3,pady=-3).grid(row=1,column=0,sticky=E)
				Button(self.mef,text='Unmount',width=10,command=lambda mnt_hostname=self.mounted_hostname[i],mnt_mountpoint=self.mounted_mountpoint[i]: self.fu_forward(mnt_hostname,mnt_mountpoint),padx=-3,pady=-3).grid(row=1,column=1,sticky=E)

	def quick_connect_reset(self):
		self.hostname_entry.delete(0,END)
		self.username_entry.delete(0,END)
		self.password_entry.delete(0,END)
		self.port_entry.delete(0,END)
		self.mountpoint_entry.delete(0,END)
		
	def feed_buffer_activity(self,buffered_text):
		self.buffer_activity.insert(END,buffered_text)
		self.buffer_activity.see(END)
		
	def feed_ftp_buffer_activity(self,ftp_buffered_text):
		self.buffer_activity.insert(END,ftp_buffered_text)
		self.buffer_activity.see(END)
		
	def choose_folder(self):
		dirname = tkFileDialog.askdirectory(parent=root,initialdir="~",title='Please select a directory')
		self.mountpoint_entry.delete(0,END)
		self.mountpoint_entry.insert(0,dirname)

	def open_folder(self,mountpoint):
		subprocess.Popen([open_cmd,mountpoint])

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
				main_gui.feed_ftp_buffer_activity(app,umnt_output)
				sys.stdout.flush()
			
		main_gui.watch_mounted(app)
		
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

if OS[0] is 0:
	fatal_error(0)
else:
	if curlftpfs is not 1:
		if OS[0] == "Linux" and unmount_cmd is 0:
			fatal_error(2)
		else:
			root=Tk()
			fuse_init=fuse_connection()
			app=main_gui(root)
			root.wm_title("gcurlftpfs - "+version)
			root.mainloop()
	else:
		fatal_error(1)
