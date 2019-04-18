import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib


import gettext
import signal

import Core
# import Dialog
import sys
import time
import threading
import os
import Dialog

signal.signal(signal.SIGINT, signal.SIG_DFL)
gettext.textdomain('first-aid-kit-gui')
_=gettext.gettext


RSRC="./rsrc/"



class FirstAidKit:
	
	
	
	def __init__(self):
		
		self.core=Core.Core.get_core()
		
	#def init
	
	
	def load_gui(self):

		
		builder=Gtk.Builder()
		builder.set_translation_domain('first-aid-kit-gui')
		ui_path=RSRC + "first-aid-kit.ui"
		builder.add_from_file(ui_path)
		
		self.main_window=builder.get_object("main_window")
		self.scrolled_window=builder.get_object("scrolledwindow3")
		self.main_box=builder.get_object("main_box")
		self.net_button=builder.get_object("net_button")
		self.hd_button=builder.get_object("hd_button")
		self.epoptes_button=builder.get_object("epoptes_button")
		self.bar_button=builder.get_object("start_bar_button1")
		self.apt_button=builder.get_object("apt_button")
		self.kernel_button=builder.get_object("kernel_button")
		self.netfiles_button=builder.get_object("netfiles_button")
		self.pmb_button=builder.get_object("pmb_button")
		
		#PANTALLA LOGIN
		self.login_da_box=builder.get_object("login_da_box")
		self.login_da=builder.get_object("login_drawingarea")
		
		self.login_overlay=Gtk.Overlay()
		self.login_overlay.add(self.login_da_box)
		
		self.login_box=builder.get_object("login_box")
		self.login_button=builder.get_object("login_button")
		self.user_entry=builder.get_object("user_entry")
		self.password_entry=builder.get_object("password_entry")
		self.login_eb_box=builder.get_object("login_eb_box")
		self.login_msg_label=builder.get_object("login_msg_label")
		self.server_ip_entry=builder.get_object("server_ip_entry")
		self.validate_spinner=builder.get_object("validate_spinner")
		
		
		self.login_overlay.add_overlay(self.login_box)
		self.login_overlay.show_all()
		
		
		
		#FIN LOGIN
		
		

		self.separator1=builder.get_object("separator1")
		self.separator3=builder.get_object("separator3")
		self.main_button_box=builder.get_object("content_box")
		self.content_subbox=builder.get_object("content_subbox")
		
		self.login_stack=Gtk.Stack()
		self.login_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.login_stack.set_transition_duration(500)
		self.main_box.pack_start(self.login_stack,True,True,0)
		
		# ADD COMPONENTS
		

		#self.login_stack.add_titled(self.login_overlay,"login","Login")
		self.login_stack.add_titled(self.main_button_box,"main_button","Main Button Box")
		
		self.main_stack=Gtk.Stack()
		self.main_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_DOWN)
		self.main_stack.set_transition_duration(500)
		self.content_subbox.pack_start(self.main_stack,True,True,5)
		
		#b=Gtk.Button("HOLA")
		#self.main_stack.add_titled(b,"hola","hola")
		try:

			#os.system('lliurex-version -f > /tmp/.FK')
			#time.sleep(0.5)
			if 'server' in open('/tmp/.FK').read():
				self.netfiles_box=self.core.netfiles_box
				self.main_stack.add_titled(self.netfiles_box,"netfilesbox","NetfilesBox")
				os.remove('/tmp/.FK')
			else:
				self.info_netfiles=builder.get_object("info_netfiles")
				self.info_netfiles_txt=builder.get_object("info_netfiles_txt")
				self.info_netfiles_txt.set_name("INFO_LABEL")
				self.info_netfiles_txt.set_text(_("Sorry you are not a server. You can't access to /net files."))
				self.main_stack.add_titled(self.info_netfiles,"netfilesbox","netfilesbox")

		except Exception as e:
			self.core.dprint("(load_gui)Error: %s"%e,"[FirstAidKit]")
			
			
		self.net_box=self.core.net_box
		self.main_stack.add_titled(self.net_box,"netbox","NetBox")
		self.hd_box=self.core.hd_box
		self.main_stack.add_titled(self.hd_box,"hdbox","HdBox")
		self.epoptes_box=self.core.epoptes_box
		self.main_stack.add_titled(self.epoptes_box,"epoptesbox","EpoptesBox")
		self.start_bar_box=self.core.start_bar_box
		self.main_stack.add_titled(self.start_bar_box,"startbarbox","StartBarBox")
		self.apt_box=self.core.apt_box
		self.main_stack.add_titled(self.apt_box,"aptbox","AptBox")
		self.kernel_box=self.core.kernel_box
		self.main_stack.add_titled(self.kernel_box,"kernelbox","KernelBox")

		self.pmb_box=self.core.pmb_box
		self.main_stack.add_titled(self.pmb_box,"pmbbox","PmbBox")

		
		self.set_css_info()
		self.connect_signals()
		#self.load_values()
		
		self.not_validate=True
		
		self.main_window.show_all()
		
		self.validate_spinner.hide()
		
		
		#NET SECTION HIDE
		#self.core.net_box.restart_txt.hide()
		self.core.net_box.configure_network_button.hide()
		self.core.net_box.configure_network_txt.hide()
		#self.core.net_box.restart_button.hide()
		#self.core.net_box.box9.hide()
		

		self.main_stack.set_visible_child_name("netbox")

	#def load_gui

		
	
	def start_gui(self):
	# LANZADOR DE LA GUI
		
		GObject.threads_init()
		Gtk.main()
		
	#def start_gui
	


	def show_main_controls(self,status):
	# OCULTA LOS CONTROLES QUE NO QUIERO QUE SEAN VISIBLES MIENTRAS NO ESTES LOGADO
	
		if status:
			self.separator1.show()
			self.separator3.show()
			self.main_button_box.show()
		else:
			self.separator1.show()
			self.separator3.hide()
			self.main_button_box.hide()
		
	#def show_main_controls
	
	
	
	
	
	def connect_signals(self):
		
		self.user_entry.connect("activate",self.entries_press_event)
		self.password_entry.connect("activate",self.entries_press_event)
		self.server_ip_entry.connect("activate",self.entries_press_event)
		self.login_button.connect("clicked",self.validate_user)
		#self.main_window.connect("destroy",Gtk.main_quit)
		#self.main_window.connect("destroy",self.close_fak) 
		self.main_window.connect("delete_event",self.close_fak)
		
		self.net_button.connect("clicked",self.net_button_clicked)
		self.hd_button.connect("clicked",self.hd_button_clicked)
		self.netfiles_button.connect("clicked",self.netfiles_button_clicked)
		self.epoptes_button.connect("clicked",self.epoptes_button_clicked)
		self.bar_button.connect("clicked",self.bar_button_clicked)
		self.apt_button.connect("clicked",self.apt_button_clicked)
		self.kernel_button.connect("clicked",self.kernel_button_clicked)
		self.pmb_button.connect("clicked",self.pmb_button_clicked)
		
	# def connect_signals
	
	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("first-aid-kit.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		self.main_window.set_name("WINDOW")
		
		self.scrolled_window.set_name("MENU_WINDOW")
		self.login_button.set_name("OPTION_BUTTON")
		self.net_button.set_name("SELECTED_OPTION_BUTTON")
		self.netfiles_button.set_name("OPTION_BUTTON")
		self.hd_button.set_name("OPTION_BUTTON")
		self.epoptes_button.set_name("OPTION_BUTTON")
		self.bar_button.set_name("OPTION_BUTTON")
		self.apt_button.set_name("OPTION_BUTTON")
		self.kernel_button.set_name("OPTION_BUTTON")
		self.pmb_button.set_name("OPTION_BUTTON")
		self.login_msg_label.set_name("ERROR_LABEL")

		self.main_button_box.set_name("GREY")
			
	#def set-css_info

	def close_fak(self,widget,event):
		try:
			if not self.core.working:
				Gtk.main_quit()
			else:
				mw=self.core.lri.main_window
				d=Dialog.InfoDialog(mw,"First Aid Kit","You can't close First Aid Kit now\nbecause you are working with the system.\nPlease wait...")
				response=d.run()
				d.destroy()
				return True

		except Exception as e:
			return 0
			self.core.dprint("(close_fak)Error: %s"%e,"[FirstAidKit]")

	#def close_fak
	
	
	#VALIDACION DEL LOGIN
	
	def entries_press_event(self,widget):
		
		self.validate_user(None)
		
	#def entries_press_event
	
	def validate_user(self,widget):
		
		self.login_msg_label.hide()
		self.validate_spinner.show()
		
		self.login_button.set_sensitive(False)
		
		self.thread=threading.Thread(target=self.validate_user_thread)
		self.thread.daemon=True
		self.thread.start()

		GLib.timeout_add(500,self.validate_user_thread_listener)
		
		
	#def validate_user
	
	def validate_user_thread(self):
		
		user=self.user_entry.get_text()
		password=self.password_entry.get_text()
		server_ip=self.server_ip_entry.get_text()
		
		# DELETE ME
		'''if user=="":
			user="netadmin"
		if password=="":
			password="lliurex"
		'''
		self.login_ret=self.core.n4d.validate_user(user,password,server_ip)
		
		print ("User: %s - Passwd: %s - Server: %s"%(user,password,server_ip))
		print self.login_ret
		
	#def validate_user_thread
	
	
	def validate_user_thread_listener(self):
		
		if self.thread.is_alive():
			return True
		
		if not self.login_ret[0]:
			self.login_msg_label.set_text("%s"%self.login_ret[1])
			self.validate_spinner.hide()
			self.login_msg_label.show()
			self.login_button.set_sensitive(True)

		else:
			
			self.validate_spinner.hide()
			self.login_stack.set_visible_child_name("main_button")
			self.main_stack.set_visible_child_name("netbox")
			#self.login_overlay.hide()
			#self.show_main_controls(True)
			self.not_validate=False
		
		return False
		
		
		
	#def validate_user_thread
	
	
	def net_button_clicked(self,widget):
		
		change_child=True
		if self.main_stack.get_visible_child_name()=="hdbox":
			selected="hd"
		if self.main_stack.get_visible_child_name()=="netfilesbox":
			selected="netfilesbox"
		if self.main_stack.get_visible_child_name()=="epoptesbox":
			selected="epoptesbox"
		if self.main_stack.get_visible_child_name()=="startbarbox":
			selected="startbarbox"
		if self.main_stack.get_visible_child_name()=="kernelbox":
			selected="kernelbox"
		if self.main_stack.get_visible_child_name()=="startbarbox":
			selected="aptbox"
		if self.main_stack.get_visible_child_name()=="pmbbox":
			selected="pmbbox"
					
		if change_child:

			self.main_stack.set_visible_child_name("netbox")
			self.net_button.set_name("SELECTED_OPTION_BUTTON")
			self.hd_button.set_name("OPTION_BUTTON")
			self.netfiles_button.set_name("OPTION_BUTTON")
			self.epoptes_button.set_name("OPTION_BUTTON")
			self.bar_button.set_name("OPTION_BUTTON")
			self.apt_button.set_name("OPTION_BUTTON")
			self.kernel_button.set_name("OPTION_BUTTON")
			self.pmb_button.set_name("OPTION_BUTTON")
		
	#def net_button_clicked
	
	
	def hd_button_clicked(self,widget):
		
		change_child=True
		if self.main_stack.get_visible_child_name()=="netbox":
			selected="netbox"
		if self.main_stack.get_visible_child_name()=="netfilesbox":
			selected="netfilesbox"
		if self.main_stack.get_visible_child_name()=="epoptesbox":
			selected="epoptesbox"
		if self.main_stack.get_visible_child_name()=="startbarbox":
			selected="startbarbox"
		if self.main_stack.get_visible_child_name()=="kernelbox":
			selected="kernelbox"
		if self.main_stack.get_visible_child_name()=="startbarbox":
			selected="aptbox"
					
		if change_child:
			self.main_stack.set_visible_child_name("hdbox")
			self.net_button.set_name("OPTION_BUTTON")
			self.hd_button.set_name("SELECTED_OPTION_BUTTON")
			self.netfiles_button.set_name("OPTION_BUTTON")
			self.epoptes_button.set_name("OPTION_BUTTON")
			self.bar_button.set_name("OPTION_BUTTON")
			self.kernel_button.set_name("OPTION_BUTTON")
			self.apt_button.set_name("OPTION_BUTTON")
			self.pmb_button.set_name("OPTION_BUTTON")
		
	#def hd_button_clicked
	
	
	def netfiles_button_clicked(self,widget):
		
		change_child=True
		if self.main_stack.get_visible_child_name()=="netbox":
			selected="netbox"
		if self.main_stack.get_visible_child_name()=="hdbox":
			selected="hdbox"
		if self.main_stack.get_visible_child_name()=="epoptesbox":
			selected="epoptesbox"
		if self.main_stack.get_visible_child_name()=="startbarbox":
			selected="startbarbox"
		if self.main_stack.get_visible_child_name()=="kernelbox":
			selected="kernelbox"
		if self.main_stack.get_visible_child_name()=="startbarbox":
			selected="aptbox"
		if self.main_stack.get_visible_child_name()=="pmbbox":
			selected="pmbbox"
					
		if change_child:
			self.main_stack.set_visible_child_name("netfilesbox")
			self.net_button.set_name("OPTION_BUTTON")
			self.hd_button.set_name("OPTION_BUTTON")
			self.netfiles_button.set_name("SELECTED_OPTION_BUTTON")
			self.epoptes_button.set_name("OPTION_BUTTON")
			self.kernel_button.set_name("OPTION_BUTTON")
			self.apt_button.set_name("OPTION_BUTTON")
			self.bar_button.set_name("OPTION_BUTTON")
			self.pmb_button.set_name("OPTION_BUTTON")
		
	#def netfiles_button_clicked
	
	
	def epoptes_button_clicked(self,widget):
		
		change_child=True
		if self.main_stack.get_visible_child_name()=="netbox":
			selected="netbox"
		if self.main_stack.get_visible_child_name()=="netfilesbox":
			selected="netfilesbox"
		if self.main_stack.get_visible_child_name()=="hdbox":
			selected="hdbox"
		if self.main_stack.get_visible_child_name()=="startbarbox":
			selected="startbarbox"
		if self.main_stack.get_visible_child_name()=="kernelbox":
			selected="kernelbox"
		if self.main_stack.get_visible_child_name()=="startbarbox":
			selected="aptbox"
		if self.main_stack.get_visible_child_name()=="pmbbox":
			selected="pmbbox"
					
		if change_child:
			self.main_stack.set_visible_child_name("epoptesbox")
			self.net_button.set_name("OPTION_BUTTON")
			self.hd_button.set_name("OPTION_BUTTON")
			self.netfiles_button.set_name("OPTION_BUTTON")
			self.epoptes_button.set_name("SELECTED_OPTION_BUTTON")
			self.kernel_button.set_name("OPTION_BUTTON")
			self.apt_button.set_name("OPTION_BUTTON")
			self.bar_button.set_name("OPTION_BUTTON")
			self.pmb_button.set_name("OPTION_BUTTON")
		
	#def epoptes_button_clicked
	
	
	def bar_button_clicked(self,widget):
		
		change_child=True
		if self.main_stack.get_visible_child_name()=="netbox":
			selected="netbox"
		if self.main_stack.get_visible_child_name()=="netfilesbox":
			selected="netfilesbox"
		if self.main_stack.get_visible_child_name()=="hdbox":
			selected="hdbox"
		if self.main_stack.get_visible_child_name()=="epoptesbox":
			selected="epoptesbox"
		if self.main_stack.get_visible_child_name()=="kernelbox":
			selected="kernelbox"
		if self.main_stack.get_visible_child_name()=="startbarbox":
			selected="aptbox"
		if self.main_stack.get_visible_child_name()=="pmbbox":
			selected="pmbbox"
					
		if change_child:
			self.main_stack.set_visible_child_name("startbarbox")
			self.net_button.set_name("OPTION_BUTTON")
			self.hd_button.set_name("OPTION_BUTTON")
			self.netfiles_button.set_name("OPTION_BUTTON")
			self.epoptes_button.set_name("OPTION_BUTTON")
			self.kernel_button.set_name("OPTION_BUTTON")
			self.apt_button.set_name("OPTION_BUTTON")
			self.bar_button.set_name("SELECTED_OPTION_BUTTON")
			self.pmb_button.set_name("OPTION_BUTTON")
		
	#def bar_button_clicked


	def kernel_button_clicked(self,widget):
		
		change_child=True
		if self.main_stack.get_visible_child_name()=="netbox":
			selected="netbox"
		if self.main_stack.get_visible_child_name()=="netfilesbox":
			selected="netfilesbox"
		if self.main_stack.get_visible_child_name()=="hdbox":
			selected="hdbox"
		if self.main_stack.get_visible_child_name()=="epoptesbox":
			selected="epoptesbox"
		if self.main_stack.get_visible_child_name()=="startbarbox":
			selected="startbarbox"
		if self.main_stack.get_visible_child_name()=="aptbox":
			selected="aptbox"
		if self.main_stack.get_visible_child_name()=="pmbbox":
			selected="pmbbox"
					
		if change_child:
			self.main_stack.set_visible_child_name("kernelbox")
			self.net_button.set_name("OPTION_BUTTON")
			self.hd_button.set_name("OPTION_BUTTON")
			self.netfiles_button.set_name("OPTION_BUTTON")
			self.epoptes_button.set_name("OPTION_BUTTON")
			self.bar_button.set_name("OPTION_BUTTON")
			self.apt_button.set_name("OPTION_BUTTON")
			self.kernel_button.set_name("SELECTED_OPTION_BUTTON")
			self.pmb_button.set_name("OPTION_BUTTON")
		
	#def kernel_button_clicked



	def apt_button_clicked(self,widget):
		
		change_child=True
		if self.main_stack.get_visible_child_name()=="netbox":
			selected="netbox"
		if self.main_stack.get_visible_child_name()=="netfilesbox":
			selected="netfilesbox"
		if self.main_stack.get_visible_child_name()=="hdbox":
			selected="hdbox"
		if self.main_stack.get_visible_child_name()=="epoptesbox":
			selected="epoptesbox"
		if self.main_stack.get_visible_child_name()=="startbarbox":
			selected="startbarbox"
		if self.main_stack.get_visible_child_name()=="kernelbox":
			selected="kernelbox"
		if self.main_stack.get_visible_child_name()=="pmbbox":
			selected="pmbbox"
					
		if change_child:
			self.main_stack.set_visible_child_name("aptbox")
			self.net_button.set_name("OPTION_BUTTON")
			self.hd_button.set_name("OPTION_BUTTON")
			self.netfiles_button.set_name("OPTION_BUTTON")
			self.epoptes_button.set_name("OPTION_BUTTON")
			self.bar_button.set_name("OPTION_BUTTON")
			self.kernel_button.set_name("OPTION_BUTTON")
			self.apt_button.set_name("SELECTED_OPTION_BUTTON")
			self.pmb_button.set_name("OPTION_BUTTON")
		
	#def apt_button_clicked


	def pmb_button_clicked(self,widget):
		
		change_child=True
		if self.main_stack.get_visible_child_name()=="netbox":
			selected="netbox"
		if self.main_stack.get_visible_child_name()=="netfilesbox":
			selected="netfilesbox"
		if self.main_stack.get_visible_child_name()=="hdbox":
			selected="hdbox"
		if self.main_stack.get_visible_child_name()=="epoptesbox":
			selected="epoptesbox"
		if self.main_stack.get_visible_child_name()=="startbarbox":
			selected="startbarbox"
		if self.main_stack.get_visible_child_name()=="kernelbox":
			selected="kernelbox"
		if self.main_stack.get_visible_child_name()=="aptbox":
			selected="aptbox"
					
		if change_child:
			self.main_stack.set_visible_child_name("pmbbox")
			self.net_button.set_name("OPTION_BUTTON")
			self.hd_button.set_name("OPTION_BUTTON")
			self.netfiles_button.set_name("OPTION_BUTTON")
			self.epoptes_button.set_name("OPTION_BUTTON")
			self.bar_button.set_name("OPTION_BUTTON")
			self.kernel_button.set_name("OPTION_BUTTON")
			self.apt_button.set_name("OPTION_BUTTON")
			self.pmb_button.set_name("SELECTED_OPTION_BUTTON")
		
	#def pmb_button_clicked
	
	
	
	
# class FirstAidKit

if __name__=="__main__":
	
	lri=FirstAidkit()
	lri.start_gui()