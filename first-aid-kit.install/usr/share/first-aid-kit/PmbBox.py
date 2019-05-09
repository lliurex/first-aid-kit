import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

import copy
import gettext
import Core

#import Dialog
import time
import threading
import sys
import os
import time
import apt

gettext.textdomain('first-aid-kit')
_=gettext.gettext


RSRC="./rsrc/"


class PmbBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('first-aid-kit')
		ui_path=RSRC + "first-aid-kit.ui"
		builder.add_from_file(ui_path)
		
		
		self.pmb_box=builder.get_object("pmb_box")
		self.pmb_box_container=builder.get_object("pmb_box_container")
		self.pmb_passwd_button=builder.get_object("pmb_passwd_button")
		self.pmb_spinner=builder.get_object("pmb_passwd_spinner")
		self.pmb_txt=builder.get_object("pmb_txt")
		self.pmb_label=builder.get_object("pmb_label")
		self.separator_pmb=builder.get_object("separator_pmb")
		
		self.info_box=builder.get_object("info_pmb")
		self.spinner_info_pmb=builder.get_object("spinner_info_pmb")
		self.txt_check_pmb=builder.get_object("txt_check_pmb")
		self.info_box_into=builder.get_object("box19")

		self.add(self.pmb_box)
		
		self.connect_signals()
		self.set_css_info()

		
		self.info_box_stack=Gtk.Stack()
		self.info_box_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.info_box_stack.set_transition_duration(500)
		hbox_pmb=Gtk.HBox()
		hbox_pmb.show()
		self.info_box_stack.add_titled(hbox_pmb,"empty_box","Empty Box")
		self.info_box_stack.add_titled(self.info_box,"infobox","InfoBox")

		self.wawabox2=Gtk.HBox()
		self.wawabox2.pack_start(self.info_box_stack,True,True,0)

		self.pmb_box.pack_start(self.wawabox2,False,False,5)


		self.info_box.set_margin_bottom(20)
		self.info_box.set_margin_left(5)
		self.info_box.set_margin_right(5)

		

		# Test if PMB is installed
		try:

			self.cache=apt.cache.Cache()
			if self.cache['pmb'].is_installed:
				self.info_box_stack.set_visible_child_name("empty_box")
				self.core.dprint("PMB it's installed","[PmbBox]")
			else:
				self.core.dprint("PMB it's NOT installed","[PmbBox]")
				self.pmb_passwd_button.set_sensitive(False)
				self.txt_check_pmb.set_text(_("PMB it's NOT installed"))
				self.info_box_stack.set_visible_child_name("infobox")
				

		except Exception as e:
			self.core.dprint("(apt_cache_test)Error: %s"%e,"[PmbBox]")
			self.pmb_passwd_button.set_sensitive(False)
			self.txt_check_pmb.set_text(_("PMB it's NOT installed or not detected"))
			self.info_box_stack.set_visible_child_name("infobox")

		#self.info_box_stack.set_visible_child_name("empty_box")
				
		
	#def __init__
	
	


	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("first-aid-kit.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		
		self.separator_pmb.set_name("SEPARATOR_MAIN")
		self.info_box.set_name("PKG_BOX")
		self.pmb_passwd_button.set_name("EXECUTE_BUTTON")
		self.pmb_box_container.set_name("PKG_BOX")
		self.pmb_txt.set_name("OPTION_LABEL")
		self.pmb_label.set_name("SECTION_LABEL")
		self.txt_check_pmb.set_name("INFO_LABEL")
			
	#def set-css_info





	def connect_signals(self):
		
		self.pmb_passwd_button.connect("clicked",self.pmb_passwd_button_clicked)
		
	#def connect_signals





	def pmb_passwd_button_clicked(self,widget):
		
		try:
			self.thread=threading.Thread(target=self.pmb_passwd_button_thread)
			self.pmb_passwd_button.set_sensitive(False)
			self.thread.daemon=True
			self.thread.start()
			
			allocation=self.pmb_passwd_button.get_allocation()
			w=allocation.width
			h=allocation.height

			self.pmb_passwd_button.hide()
			self.pmb_spinner.start()
			self.pmb_spinner.set_size_request(w,h)
			self.pmb_spinner.show()

			self.info_box_stack.set_visible_child_name("infobox")
			self.txt_check_pmb.set_text(_("You're resetting admin passwd to PMB, please wait...."))

			GLib.timeout_add(500,self.check_pmb_passwd_button_thread)

		except Exception as e:
			self.core.dprint("(pmb_passwd_button_clicked)Error: %s"%e,"[PmbBox]")
			return False
	
	#pmb_execute_button_clicked



	def pmb_passwd_button_thread(self):
	
		try:
			self.core.working=True
			self.core.dprint("Reseting your PMB passwd.........","[PmbBox]")
			os.system('mysql -s -N -e "update pmb.users set pwd=password(\'admin\') where username like \'admin\';"')
			time.sleep(1)
			self.thread_ret={"status":True,"msg":"BROKEN"}
			
		except Exception as e:
			self.core.dprint("(pmb_passwd_button_thread)Error: %s"%e,"[PmbBox]")
			return False
			
	#def pmb_execute_button_thread


	def check_pmb_passwd_button_thread(self):
		
		try:
			if self.thread.is_alive():
				return True
		
			self.core.working=False

			self.pmb_spinner.hide()
			self.pmb_passwd_button.show()
			self.pmb_passwd_button.set_sensitive(True)
			self.info_box_stack.set_visible_child_name("empty_box")
			self.info_box_stack.set_visible_child_name("infobox")
			self.txt_check_pmb.set_text(_("Your new passwd to admin user is admin\nPlease logged in your application and change it."))
			self.core.dprint("Your new passwd to admin user is admin. Please logged in your application and change it.","[PmbBox]")

		except Exception as e:
			self.core.dprint("(check_pmb_execute_button_thread)Error: %s"%e,"[PmbBox]")
			return False
		
	#check_pmb_execute_button_thread
