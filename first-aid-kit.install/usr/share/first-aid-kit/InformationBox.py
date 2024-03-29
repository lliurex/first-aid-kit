import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

import copy
import gettext
import Core
import platform
import psutil

#import Dialog
import time
import threading
import sys
import os
import subprocess
import time
import apt
import cpuinfo
import textwrap
import socket
import pwd
import grp

gettext.textdomain('first-aid-kit')
_=gettext.gettext


RSRC="./rsrc/"


class InformationBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('first-aid-kit')
		ui_path=RSRC + "first-aid-kit.ui"
		builder.add_from_file(ui_path)
		
		
		self.information_box=builder.get_object("information_box")
		self.information_box_container=builder.get_object("information_box_container")
		self.information_box_container_grid=builder.get_object("information_box_container_grid")
		self.information_box_grid=builder.get_object("information_box_grid")
		self.information_vp=builder.get_object("information_viewport")
		self.information_sw=builder.get_object("information_scrolled")
		self.information_list_box=builder.get_object("information_box_vp")

		self.information_title=builder.get_object("information_title")
		self.information_title2=builder.get_object("information_title2")
		self.information_label_release=builder.get_object("information_label_release")
		self.information_label_timestamp=builder.get_object("information_label_timestamp")
		self.information_label_kernel=builder.get_object("information_label_kernel")
		self.information_label_ram=builder.get_object("information_label_ram")
		self.informationv_label_cpu_model=builder.get_object("information_label_cpu_model")
		self.information_label_meta=builder.get_object("information_label_meta")
		self.information_label_flavour=builder.get_object("information_label_flavour")
		self.information_label_cpu_speed=builder.get_object("information_label_cpu_speed")
		self.information_label_cpu_core=builder.get_object("information_label_cpu_core")
		self.information_pinning_title=builder.get_object("information_pinning_title")
		
		self.information_hdd_filesystem=builder.get_object("information_hdd_filesystem")
		self.information_hdd_type=builder.get_object("information_hdd_type")
		self.information_hdd_size=builder.get_object("information_hdd_size")
		self.information_hdd_used=builder.get_object("information_hdd_used")
		self.information_hdd_avail=builder.get_object("information_hdd_avail")
		self.information_hdd_use=builder.get_object("information_hdd_use")

		self.information_label_release_solved=builder.get_object("information_label_release_solved")
		self.information_label_timestamp_solved=builder.get_object("information_label_timestamp_solved")
		self.information_label_kernel_solved=builder.get_object("information_label_kernel_solved")
		self.information_label_ram_solved=builder.get_object("information_label_ram_solved")
		self.informationv_label_cpu_model_solved=builder.get_object("information_label_cpu_model_solved")
		self.information_label_meta_solved=builder.get_object("information_label_meta_solved")
		self.information_label_flavour_solved=builder.get_object("information_label_flavour_solved")
		self.information_label_cpu_speed_solved=builder.get_object("information_label_cpu_speed_solved")
		self.information_label_cpu_core_solved=builder.get_object("information_label_cpu_core_solved")
		self.information_pinning_title_solved=builder.get_object("information_pinning_title_solved")

		self.information_center_code_solved_2=builder.get_object("center_code_solved")
		self.information_center_code_title=builder.get_object("center_code_solved_title")
		self.information_classroom_code_solved=builder.get_object("information_clasroom_code_solved")
		self.information_classroom_code_title=builder.get_object("information_classroom_code_title")


		self.information_label_release_solved.set_text(_("Unknow"))
		self.information_label_timestamp_solved.set_text(_("Unknow"))
		self.information_label_kernel_solved.set_text(_("Unknow"))
		self.information_label_ram_solved.set_text(_("Unknow"))
		self.informationv_label_cpu_model_solved.set_text(_("Unknow"))
		self.information_label_meta_solved.set_text(_("Unknow"))
		self.information_label_flavour_solved.set_text(_("Unknow"))
		self.information_label_cpu_speed_solved.set_text(_("Unknow"))
		self.information_pinning_title_solved.set_text(_("Unknow"))
		self.information_center_code_solved_2.set_text(_("Unknow"))
		self.information_classroom_code_solved.set_text(_("Unknow"))

		self.separator_information=builder.get_object("separator_information")
		self.separator_information2=builder.get_object("separator_information2")

		self.info_box=builder.get_object("info_information")
		self.spinner_information=builder.get_object("spinner_information")
		self.txt_check_information=builder.get_object("txt_check_information")
		self.info_box_into=builder.get_object("box6")


		self.add(self.information_box)
		
		#self.connect_signals()
		self.set_css_info()

		
		self.info_box_stack=Gtk.Stack()
		self.info_box_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.info_box_stack.set_transition_duration(500)
		hbox_information=Gtk.HBox()
		hbox_information.show()
		self.info_box_stack.add_titled(hbox_information,"empty_box","Empty Box")
		self.info_box_stack.add_titled(self.info_box,"infobox","InfoBox")


		self.information_box_stack=Gtk.Stack()
		self.information_box_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.information_box_stack.set_transition_duration(500)
		#load_spinner=Gtk.Spinner()
		#load_spinner.show()
		#load_spinner.start()
		#self.kernel_box_stack.add_titled(load_spinner,"spinner","")
		self.information_box_stack.add_titled(self.information_list_box,"kernels","")
		self.information_vp.add(self.information_box_stack)

		self.wawabox2=Gtk.HBox()
		self.wawabox2.pack_start(self.info_box_stack,True,True,0)

		self.information_box.pack_start(self.wawabox2,False,False,5)


		self.info_box.set_margin_bottom(5)
		self.info_box.set_margin_left(5)
		self.info_box.set_margin_right(5)

		self.information_system()
				
		
	#def __init__
	
	


	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("first-aid-kit.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		
		self.separator_information.set_name("SEPARATOR_MAIN")
		self.separator_information2.set_name("SEPARATOR_MAIN")
		self.info_box.set_name("PKG_BOX")
		self.information_box_container.set_name("PKG_BOX")
		self.information_list_box.set_name("PKG_BOX")
		self.information_title.set_name("SECTION_LABEL")
		self.information_title2.set_name("SECTION_LABEL")

		self.information_label_release.set_name("OPTION_LABEL")
		self.information_label_timestamp.set_name("OPTION_LABEL")
		self.information_label_kernel.set_name("OPTION_LABEL")
		self.information_label_ram.set_name("OPTION_LABEL")
		self.informationv_label_cpu_model.set_name("OPTION_LABEL")
		self.information_label_meta.set_name("OPTION_LABEL")
		self.information_label_flavour.set_name("OPTION_LABEL")
		self.information_label_cpu_speed.set_name("OPTION_LABEL")
		self.information_label_cpu_core.set_name("OPTION_LABEL")
		self.information_pinning_title.set_name("OPTION_LABEL")
		self.information_center_code_title.set_name("OPTION_LABEL")
		self.information_classroom_code_title.set_name("OPTION_LABEL")
		#self.information_pinning_title_solved.set_name("INFO_LABEL")

		self.information_hdd_filesystem.set_name("OPTION_LABEL")
		self.information_hdd_type.set_name("OPTION_LABEL")
		self.information_hdd_size.set_name("OPTION_LABEL")
		self.information_hdd_used.set_name("OPTION_LABEL")
		self.information_hdd_avail.set_name("OPTION_LABEL")
		self.information_hdd_use.set_name("OPTION_LABEL")

		self.txt_check_information.set_name("INFO_LABEL")

		#self.txt_check_pmb.set_name("INFO_LABEL")
			
	#def set-css_info


	

	def information_system(self):
		try:

			self.information_list_box.set_margin_bottom(20)
			self.information_list_box.set_margin_top(5)
			self.information_list_box.set_margin_left(9)
			self.information_list_box.set_margin_right(9)

			self.thread=threading.Thread(target=self.information_system_thread)
			self.thread.daemon=True
			self.thread.start()

			self.core.dprint("Reading system information..........","[InformationBox]")
			GLib.timeout_add(1000,self.check_information_system_thread)

								

		except Exception as e:
			self.core.dprint("[InformationBox](information_system)Error: %s"%e)
		
	#def information_system

	

	def information_system_thread(self):
		try:
			
			self.cpu=self.cpu_info_function()

			self.read_hdd()
			#kernel version in use
			self.information_label_kernel_function()

			self.information_label_ram_function()

			self.information_label_release_function()

			self.information_center_code_function()

			self.information_label_timestamp_function()

			self.information_pinning_title_function()

			server_test=self.information_label_flavour_function()	
			self.information_label_meta_function()
			if server_test[0]:
				if ( 'server' in server_test[1] ):
					self.information_info_model_server()
				if ( 'client' in server_test[1] ):
					self.information_info_mount_client()

		except Exception as e:
			self.core.dprint("[InformationBox](information_system_thread)Error: %s"%e)
		
	#def information_system_thread


	def check_information_system_thread(self):
		
		try:
			if self.thread.is_alive():
				return True

			self.informationv_label_cpu_model_function(self.cpu)

			self.information_label_cpu_speed_function(self.cpu)

		except Exception as e:
			self.core.dprint("(check_information_system_thread) Error: %s"%e,"[InformationBox]")

	#def check_information_system_thread



	def information_label_release_function(self):
		
		try:
			release_solved=subprocess.check_output(['lliurex-version','-n']).decode('utf-8').split('.')[0]
			release_solved=release_solved.replace('\n',"")
			self.information_label_release_solved.set_text('LlX'+release_solved)

		except Exception as e:
			self.information_label_release_solved.set_text('Unknow')
			self.core.dprint("[InformationBox](information_label_release_function)Error: %s"%e)
		
	#def information_label_release_function


	def information_label_timestamp_function(self):
		
		try:
			timestamp_solved=subprocess.check_output(['lliurex-version','-n']).decode('utf-8').split()[0]
			self.information_label_timestamp_solved.set_text(timestamp_solved)

		except Exception as e:
			self.information_label_timestamp_solved.set_text('Unknow')
			self.core.dprint("[InformationBox](information_label_timestamp_function)Error: %s"%e)
		
	#def information_label_timestamp_function

	def information_label_meta_function(self):
		
		try:
			list_meta_solved = os.popen("lliurex-version --history").readlines()
			history={}
			count=0
			for item in list_meta_solved:
				words=item.split()
				history[count]={}
				history[count]['operation']=words[0]
				history[count]['meta']=words[1]
				history[count]['date']=words[2]
				history[count]['time']=words[3]
				count=count+1

			try:
				if history[0]['operation'] == '+':
					label_meta_solved=history[0]['meta']
				else:
					label_meta_solved='Uninstalled'

			except Exception as e:
				label_meta_solved='Unknow'

			self.information_label_meta_solved.set_text(label_meta_solved)
			list_meta_solved_tooltip=subprocess.check_output(['lliurex-version','--history']).decode('utf-8')
			self.information_label_meta_solved.set_property("tooltip-text", list_meta_solved_tooltip)

		except Exception as e:
			self.core.dprint("[InformationBox](information_label_meta_function)Error: %s"%e)
		
	#def information_label_cpu_cores_function


	def information_info_model_server(self):
		# If is a Server show model, Master/Slave Aula Model or Centre Model
		try:
			server_master=_("Master")
			center_model=_("Classroom")
			net_export=_('Local')

			#check if /net is local, exported or imported
			list_exportfs = os.popen("exportfs").readlines()
			if os.path.isfile('/etc/auto.lliurex'):
				list_importfs = os.popen("cat /etc/auto.lliurex").readlines()
				for lineimport in list_importfs:
					if '/net/server-sync' in lineimport:
						lineimport= list(lineimport.split())
						ip_import=lineimport[2].rsplit(':', 1)[0]
						net_export=_('Imported from ')
						net_export=net_export+ip_import
						break
			else:
				for linefs in list_exportfs:
					if '/net/server-sync' in linefs:
						net_export=_('Exported')
						break
			#Check if Server is Master/slave and Clashroom Model/ Center Model
			list_ldap = os.popen("ldapsearch -Y EXTERNAL -H ldapi:// -b cn=config").readlines()
			for line in list_ldap:
				if 'rid=' in line:
					server_master=_("Slave")
					center_model=_("Center")
					break
				else:
					server_master=_("Master")
					if 'syncprov' in line:
						center_model=_("Center")
					else:
						server_master=_("Independent")
						center_model=_("Classroom")

			
			'''if os.path.isfile('/etc/apt/preferences.d/lliurex-pinning'):
				pinning=_('Active')
			else:
				pinning=_('Removed')'''

					
			self.txt_check_information.set_text('Server: '+server_master+'    ---    Model: '+center_model+'    ---    /net: '+net_export)
			self.info_box_stack.set_visible_child_name("infobox")

		except Exception as e:
			server_master=_("Unknow")
			center_model=_("Unknow")
			net_export=_('Unknow')
			pinning=_('Unknow')
			self.core.dprint("(information_info_model_server)Error: %s"%e,"[InformationBox]")
			self.txt_check_information.set_text(_("Detection server has errors."))
			self.info_box_stack.set_visible_child_name("infobox")

	#def information_info_model_server


	def information_info_mount_client(self):
		# If is a client show mount information
		try:
			client=_("Client")
			bind_net=_("Mounted")
			documents=_('Mounted')
			server_ip=socket.gethostbyname('server')
			user_run_list=[]
			tested_list=[]

			#List users mounted in /run
			list_mount = os.popen("mount").readlines()
			for lineimport in list_mount:
				if server_ip in lineimport:
					if 'run' in lineimport:
						linewords=lineimport.split()
						for phrase in linewords:
							if 'run' in phrase:
								words=phrase.split('/')
								user=words[2]
								if user not in user_run_list:
									user_run_list.append(user)
								

			#print('Users mounted: %s'%user_run_list)

			for user in user_run_list:
				path_run=''
				user_groups=self.getgroups(user)
				#print(user)
				#print(type(user))
				#print(user_groups)
				if user_groups[0]:
					if 'students' in user_groups[1]:
						#/run/alu02/home/students/alu02/Documents/
						path_run='/run/'+user+'/home/students/'+user+'/Documents/'
					elif 'teachers' in user_groups[1]:
						#/run/alu02/home/students/alu02/Documents/
						path_run='/run/'+user+'/home/teachers/'+user+'/Documents/'
					elif 'admins' in user_groups[1]:
						#/run/alu02/home/students/alu02/Documents/
						path_run='/run/'+user+'/home/admins/'+user+'/Documents/'
				else:
					print('(information_info_mount_client)Error: No group detected')
					self.txt_check_information.set_text(_("No group detected."))
					self.info_box_stack.set_visible_child_name("infobox")
					return True
				
				#print(path_run)
				tested=self.test_mount(user,path_run)
				if tested:
					self.core.dprint('%s: All mounted OK'%user,"[InformationBox]")
					tested_list.append(user)
				else:
					self.core.dprint('%s: Fail, not mounted'%user,"[InformationBox]")

			#print(tested_list)
			if not tested_list:
				self.txt_check_information.set_text('No directory mounted')
			else:
				self.txt_check_information.set_text('Mounted ok to: %s'%tested_list)
			
			self.info_box_stack.set_visible_child_name("infobox")

		except Exception as e:
			server_master=_("Unknow")
			center_model=_("Unknow")
			net_export=_('Unknow')
			pinning=_('Unknow')
			self.core.dprint("(information_info_mount_client)Error: %s"%e,"[InformationBox]")
			self.txt_check_information.set_text(_("Information mount client error."))
			self.info_box_stack.set_visible_child_name("infobox")

	#def information_info_mount_client




	def getgroups(self,user):
		try:
			gids = [g.gr_gid for g in grp.getgrall() if user in g.gr_mem]
			gid = pwd.getpwnam(user).pw_gid
			gids.append(grp.getgrgid(gid).gr_gid)
			user_groups=[grp.getgrgid(gid).gr_name for gid in gids]
			return [True, user_groups]

		except Exception as e:
			self.core.dprint("(getgroups)Error: %s"%e,"[InformationBox]")
			user_groups=[]
			return [False, user_groups]
	#def getgroups


	def test_mount(self,user,path_run):
		try:
			test_file='test_FAK.txt'
			path_test=path_run+test_file
			tested=False

			if os.path.isdir(path_run):
				open(path_test, 'x')
			else:
				print('Path RUN not exists')
				return False 

			for document in ['Documents','Documentos','Document']:
				path_home='/home/'+user+'/'+document
				if os.path.isdir(path_home):
					if os.path.isfile(path_home+'/'+test_file):
						tested=True
			os.remove(path_test)

			return tested

		except Exception as e:
			self.core.dprint("(test_mount)Error: %s"%e,"[InformationBox]")
			return False
	#def test_mount




	def information_pinning_title_function(self):
		
		try:
			if self.core.pinning():
				pinning=_('Active')
				self.information_pinning_title_solved.set_name("")
			else:
				pinning=_('Disabled')
				self.information_pinning_title_solved.set_name("INFO_LABEL_ERROR")
			self.information_pinning_title_solved.set_text(pinning)
		except Exception as e:
			self.core.dprint("(information_info_model_server)Error pinning detection: %s"%e,"[InformationBox]")
			self.information_pinning_title_solved.set_text(_("Unknow"))
		
	#def information_pinning_title_function

	def information_pinning_title_function_change(self,pinning,csstype):
		
		self.information_pinning_title_solved.set_name(csstype)
		self.information_pinning_title_solved.set_text(pinning)

	#def information_pinning_title_function_change



	def information_label_kernel_function(self):
		
		try:
			self.information_label_kernel_solved.set_text(platform.release())

		except Exception as e:
			self.core.dprint("[InformationBox](information_label_kernel_function)Error: %s"%e)
		
	#def information_label_kernel_function



	def information_label_ram_function(self):
		
		try:
			raminstalled=round(dict(psutil.virtual_memory()._asdict())['total']/(1024*1024*1024), 1)
			self.information_label_ram_solved.set_text(str(raminstalled)+' GB')

		except Exception as e:
			self.core.dprint("[InformationBox](information_label_ram_function)Error: %s"%e)
		
	#def information_label_ram_function


	def cpu_info_function(self):
		
		try:
			cpu=cpuinfo.get_cpu_info()
			return cpu

		except Exception as e:
			self.core.dprint("[InformationBox](cpu_info_function)Error: %s"%e)
		
	#def cpu_info_function



	def informationv_label_cpu_model_function(self,cpu):
		
		try:
			cpu_model=cpu['brand']
			cpu_model_solved=cpu_model.rsplit('@', 1)[0]
			self.informationv_label_cpu_model_solved.set_text(cpu_model_solved)

		except Exception as e:
			self.core.dprint("[InformationBox](informationv_label_cpu_model_function)Error: %s"%e)
		
	#def informationv_label_cpu_model_function



	def information_label_cpu_speed_function(self,cpu):
		
		try:
			cpu_model=cpu['brand']
			cpu_speed_solved=cpu_model.rsplit('@', 1)[1]
			cpu_cores_solved=str(cpu['count'])
			self.information_label_cpu_speed_solved.set_text(cpu_speed_solved)
			self.information_label_cpu_core_solved.set_text(cpu_cores_solved)

		except Exception as e:
			self.core.dprint("[InformationBox](information_label_cpu_speed_function)Error: %s"%e)
		
	#def information_label_cpu_speed_function
	


	def information_label_flavour_function(self):
		
		try:
			flavour_solved=subprocess.check_output(['lliurex-version','-f']).decode('utf-8').split()[0]
			self.information_label_flavour_solved.set_text(flavour_solved)
			if ( 'Server' in flavour_solved ) or ( 'server' in flavour_solved ):
				return [True, "server"]
			elif ( 'Client' in flavour_solved ) or ( 'client' in flavour_solved ):
				return [True, "client"]
			else:
				return False

		except Exception as e:
			self.information_label_flavour_solved.set_text('Unknow')
			self.core.dprint("[InformationBox](information_label_flavour_function)Error: %s"%e)
		
	#def information_label_ram_function


	def read_hdd (self):

		try:
			list_hd = os.popen("LANGUAGE=en; df -T -h").readlines()
			for element_hd in list_hd:
				if not 'tmpfs' in element_hd:
					if not 'Type' in element_hd:
						element_hd= list(element_hd.split())
						#print (element_hd)
						self.generate_element_list(element_hd)
						

		except Exception as e:
			self.core.dprint("[InformationBox](read_hdd)Error: %s"%e)

	#def read_hdd

	def generate_element_list(self,element_hd):
		try:
			hbox=Gtk.Box(homogeneous=True)

			if len(element_hd[0]) > 14:
				label_name=textwrap.wrap(element_hd[0], width=14)[0]+'...'
				label_name=Gtk.Label(label_name)
			else:
				label_name=Gtk.Label(element_hd[0])
			label_name.set_property("tooltip-text", element_hd[0]+'  mounted on  '+element_hd[6])
			hbox.pack_start(label_name,True,True,0)

			label_type=Gtk.Label(element_hd[1])
			hbox.pack_start(label_type,True,True,0)

			label_size=Gtk.Label(element_hd[2])
			hbox.pack_start(label_size,True,True,0)

			label_used=Gtk.Label(element_hd[3])
			hbox.pack_start(label_used,True,True,0)

			label_avail=Gtk.Label(element_hd[4])
			hbox.pack_start(label_avail,True,True,0)

			label_mounted=Gtk.Label(element_hd[5])
			hbox.pack_start(label_mounted,True,True,0)

			hbox.set_margin_left(10)
			hbox.set_margin_right(10)
			hbox.show_all()

			tmp=Gtk.EventBox()
			tmp.add(hbox)
			tmp.show_all()
			tmp.add_events( Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK )
			tmp.connect("motion-notify-event",self.mouse_over_hdd)
			tmp.connect("leave_notify_event",self.mouse_left_hdd)
			self.information_list_box.pack_start(tmp,False,False,5)

		except Exception as e:
			self.core.dprint("(generate_element_list) Error: %s"%e,"[InformationBox]")
	
	#def generate_element_list


	def mouse_over_hdd(self,eb,event):

		eb.set_name("KERNEL_OVER")

	#def mouse_over_kernel


	def mouse_left_hdd(self,eb,event):

		eb.set_name("KERNEL_REGULAR")

	#def mouse_over_kernel


	def information_center_code_function(self):
		
		try:
			code_solved=subprocess.check_output(['client-register','-s']).decode('utf-8').split('.')[0]
			for line in code_solved.splitlines():
				if "Center" in line:
					#print(line.rsplit(':', 1)[1])
					center_code_solved_bash=line.rsplit(':', 1)[1].strip()
					self.information_center_code_solved_2.set_text(center_code_solved_bash)
				if "Aula" in line:
					#print(line.rsplit(':', 1)[1])
					classroom_code_solved=line.rsplit(':', 1)[1].strip()
					self.information_classroom_code_solved.set_text(classroom_code_solved)

		except Exception as e:
			self.information_center_code_solved_2.set_text(_("Unknow"))
			self.information_classroom_code_solved.set_text(_("Unknow"))
			self.core.dprint("[InformationBox](information_center_code_function)Error: %s"%e)
		
	#def information_center_code_function
