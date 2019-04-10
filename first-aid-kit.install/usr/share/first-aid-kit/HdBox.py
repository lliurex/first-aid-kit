import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

import copy
import gettext
import Core

import Dialog
import time
import threading
import sys
import os

gettext.textdomain('first-aid-kit-gui')
_=gettext.gettext


RSRC="./rsrc/"


class HdBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('first-aid-kit-gui')
		ui_path=RSRC + "first-aid-kit.ui"
		builder.add_from_file(ui_path)
		
		
		self.hd_box=builder.get_object("hd_box")
		self.hd_box10=builder.get_object("box10")
		self.gparted_button=builder.get_object("gparted_button")
		self.fsck_button=builder.get_object("fsck_button")
		self.txt_check_netfiles=builder.get_object("txt_check_hd")
		self.spinner_netfiles=builder.get_object("spinner_hd")
		self.label11=builder.get_object("label11")
		self.label12=builder.get_object("label12")
		self.section_label_2=builder.get_object("section_label_2")
		self.gparted_spinner=builder.get_object("gparted_spinner")
		self.gparted_box=builder.get_object("gparted_box")
		self.hdbox_check=builder.get_object("info_box")
		self.hdbox_check_into=builder.get_object("box12")
		self.separator7=builder.get_object("separator7")

		

		self.add(self.hd_box)
		
		self.hdbox_check_stack=Gtk.Stack()
		self.hdbox_check_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.hdbox_check_stack.set_transition_duration(500)
		hbox=Gtk.HBox()
		hbox.show()
		self.hdbox_check_stack.add_titled(hbox,"empty_box","Empty Box")
		self.hdbox_check_stack.add_titled(self.hdbox_check,"hdboxcheck","HDboxCheck")

		self.wawabox=Gtk.HBox()
		self.wawabox.pack_start(self.hdbox_check_stack,True,True,0)

		self.hd_box.pack_start(self.wawabox,False,False,5)


		self.hdbox_check.set_margin_bottom(20)
		self.hdbox_check.set_margin_left(5)
		self.hdbox_check.set_margin_right(5)

		self.connect_signals()
		self.set_css_info()

		
		#test fsck
		self.fsck_path='/forcefsck'
		if not os.path.exists(self.fsck_path):
			self.fsck=False
			self.fsck_button.set_label(_("Enable"))
			self.hdbox_check_stack.set_visible_child_name("empty_box")
		else:
			self.fsck=True
			self.fsck_button.set_label(_("Disable"))
			self.hdbox_check_stack.set_visible_child_name("hdboxcheck")
			self.txt_check_netfiles.set_text(_("Programmed a fscky in principal HD on the reboot"))
		




	#def __init__
	
	
	
	
	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("first-aid-kit.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		

		self.gparted_button.set_name("EXECUTE_BUTTON")
		self.fsck_button.set_name("EXECUTE_BUTTON")
		self.hd_box10.set_name("PKG_BOX")
		self.separator7.set_name("SEPARATOR_MAIN")
		#self.hdbox_check_into.set_name("PKG_BOX")
		self.hdbox_check.set_name("PKG_BOX")
		#self.wawabox.set_name("PKG_BOX")

		self.label11.set_name("OPTION_LABEL")
		self.label12.set_name("OPTION_LABEL")
		self.section_label_2.set_name("SECTION_LABEL")
		self.txt_check_netfiles.set_name("INFO_LABEL")
			
	#def set-css_info
	
	
	
	
	def connect_signals(self):
		
		self.gparted_button.connect("clicked",self.gparted_button_clicked)
		self.fsck_button.connect("clicked",self.fsck_button_clicked)
		
	#def connect_signals
	


	def gparted_button_clicked(self,widget):
		
		self.thread=threading.Thread(target=self.gparted_button_thread)
		self.gparted_button.set_sensitive(False)
		self.thread.daemon=True
		self.thread.start()
		
		allocation=self.gparted_button.get_allocation()
		w=allocation.width
		h=allocation.height

		self.gparted_button.hide()
		self.gparted_spinner.start()
		self.gparted_spinner.set_size_request(w,h)
		self.gparted_spinner.show()

		GLib.timeout_add(500,self.check_gparted_thread)
	
	#def_gparted_button_clicked



	def gparted_button_thread(self):
	
		try:
			self.core.working=True
			self.core.dprint("Opening Partition Manager for HD....","[HdBox]")

			if self.core.current_session=='lliurex-mate':
				os.system('gparted')
			else:
				os.system('partitionmanager')

			self.thread_ret={"status":True,"msg":"BROKEN"}
			
		except Exception as e:
			self.core.dprint("(gparted_button_thread)Error: %s"%e,"[HdBox]")
			return False
			
	#def gparted_button_thread


	def check_gparted_thread(self):
		
		if self.thread.is_alive():
			return True
		
		self.core.working=False
		self.gparted_spinner.hide()
		self.gparted_button.show()
		self.gparted_button.set_sensitive(True)
		
	#check_gparted_thread




	def fsck_button_clicked(self,widget):
		

		

		if self.fsck == False:
			os.system('touch %s'%self.fsck_path)
			self.fsck_button.set_label(_("Disable"))
			self.fsck = True
			self.hdbox_check_stack.set_visible_child_name("hdboxcheck")
			self.txt_check_netfiles.set_text(_("Programmed a fscky in principal HD on the reboot"))
			#self.txt_check_netfiles.show()
		else:
			os.system('rm %s'%self.fsck_path)
			self.fsck_button.set_label(_("Enable"))
			self.fsck = False
			self.hdbox_check_stack.set_visible_child_name("empty_box")
	
	#def_fsck_button_clicked
	
	
	