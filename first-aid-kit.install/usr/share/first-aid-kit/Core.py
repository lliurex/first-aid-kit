import FirstAidKit
import logging
import NetBox
import HdBox
import NetfilesBox
import EpoptesBox
import StartBarBox
import KernelBox
import N4dManager
import AptBox
import os
import subprocess
import pwd
import sys
import Dialog

class Core:
	
	singleton=None
	DEBUG=True
	os.chdir(sys.path[0])
	working=False

	logging.basicConfig(format = '%(asctime)s %(message)s',datefmt = '%m/%d/%Y %I:%M:%S %p',filename = '/var/log/first-aid-kit.log',level=logging.DEBUG)

	
	@classmethod
	def get_core(self):
		
		if Core.singleton==None:
			Core.singleton=Core()
			Core.singleton.init()

		return Core.singleton
		
	
	def __init__(self,args=None):

		self.dprint("                                  ")
		self.dprint("----------------------------------")
		self.dprint("********* First Aid Kit **********")
		
		
		self.var=None
		self.acl_time_path="/tmp/.fak_acl_timepath"

		self.get_current_user()
		self.get_other_info()
		self.get_n4d_key()

		self.dprint("User: %s"%self.current_user)
		self.dprint("User: %s"%self.current_session)
		self.dprint("----------------------------------")
		self.dprint("                                  ")

	#def __init__


	def get_n4d_key(self):

		try:
			f=open("/etc/n4d/key")
			self.n4d_key=f.readline().strip("\n")
			f.close()
			#print ("validacion: %s"%self.n4d_key)
		except Exception as e:
			print(str(e))
			sys.exit(1)

	#def get_n4d_key


	def get_other_info(self):

		#discover the desktop session
		env_file="/tmp/.first-aid-kit.%s"%self.current_user
		f=open(env_file)
		lines=f.readlines()
		f.close()
		os.remove(env_file)
		self.xwindows_access=False
		for line in lines:
			if "DESKTOP_SESSION=" in line:
				self.current_session=line.split("=")[1].strip("\n")
				self.xwindows_access=True
				
		if not self.xwindows_access:
			self.current_session=False
			d=Dialog.InfoDialog(None,"First Aid Kit","Sorry this user can't access to Xwindows,\nplease login with another one.")
			d.run()
			d.destroy()
			sys.exit(1)

		#discover if you are a server
		lliurex_version="/tmp/.FK.%s"%self.current_user
		os.system('lliurex-version -f > %s'%lliurex_version)

		#IS SERVER?
		if 'server' in open(lliurex_version).read():
			self.server=True
		else:
			self.server=False
		os.remove(lliurex_version)


		os.system('lliurex-version > %s'%lliurex_version)
		#IS XENIAL?
		if '16.' in open(lliurex_version).read():
			self.xenial=True
			self.restart_net="systemctl restart networking"
			self.configure_net=""
		else:
			self.xenial=False
			self.restart_net="sleep 3"
			self.configure_net=""

		os.remove(lliurex_version)



	#def get_useful_info


	def get_current_user(self):

		if "PKEXEC_UID" in os.environ:
			self.current_user=pwd.getpwuid(int(os.environ["PKEXEC_UID"])).pw_name
		else:
			self.current_user=os.environ["SUDO_USER"]

	#def get_current_user



	
	def init(self):
		
		self.dprint("Creating N4D client...")
		self.n4d=N4dManager.N4dManager()
		
		self.dprint("Creating NetBox...")
		self.net_box=NetBox.NetBox()
		
		self.dprint("Creating HdBox...")
		self.hd_box=HdBox.HdBox()
		
		self.dprint("Creating EpoptesBox...")
		self.epoptes_box=EpoptesBox.EpoptesBox()
		
		self.dprint("Creating StartBarBox...")
		self.start_bar_box=StartBarBox.StartBarBox()

		self.dprint("Creating KernelBox...")
		self.kernel_box=KernelBox.KernelBox()

		self.dprint("Creating AptBox...")
		self.apt_box=AptBox.AptBox()
		
		os.system('lliurex-version -f > /tmp/.FK')
		if self.server:
			self.dprint("Creating NetfilesBox...")
			self.netfiles_box=NetfilesBox.NetfilesBox()
		
		# ####
		
		# #########
		
		# Main window must be the last one
		self.dprint("Creating First Aid Kit...")
		self.lri=FirstAidKit.FirstAidKit()
		
		self.lri.load_gui()
		if self.server:
			self.netfiles_box.check_thread_on_startup()

		self.lri.start_gui()

		
		
	#def init
	
	
	
	def dprint(self,msg,module="[CORE]"):

		try:
			logging.debug("%s %s"%(module,msg))
		
			if Core.DEBUG:
			
				print("%s %s"%(module,msg))

		except Exception as e:
			print("([CORE] dprint) Error: %e")
	
	#def  dprint

	def lprint(self,msg,module="[CORE]"):
		try:

			logging.debug("%s %s"%(module,msg))

		except Exception as e:
			print("([CORE] lprint) Error: %e")
		
	#def lprint