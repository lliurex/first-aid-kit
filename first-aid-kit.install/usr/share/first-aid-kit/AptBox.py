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

gettext.textdomain('first-aid-kit-gui')
_=gettext.gettext


RSRC="./rsrc/"


class AptBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('first-aid-kit-gui')
		ui_path=RSRC + "first-aid-kit.ui"
		builder.add_from_file(ui_path)
		
		
		self.apt_box=builder.get_object("apt_box")
		self.apt_box7=builder.get_object("box7")
		self.apt_execute_button=builder.get_object("apt_execute_button")
		self.apt_spinner=builder.get_object("apt_spinner")
		self.apt_txt=builder.get_object("apt_txt")
		self.apt_label=builder.get_object("apt_label")
		self.separator4=builder.get_object("separator4")
		
		self.info_box=builder.get_object("info_apt")
		self.spinner_apt=builder.get_object("spinner_apt")
		self.txt_check_apt=builder.get_object("txt_check_apt")
		self.info_box_into=builder.get_object("box17")

		self.add(self.apt_box)
		
		self.connect_signals()
		self.set_css_info()

		
		self.info_box_stack=Gtk.Stack()
		self.info_box_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.info_box_stack.set_transition_duration(500)
		hbox_apt=Gtk.HBox()
		hbox_apt.show()
		self.info_box_stack.add_titled(hbox_apt,"empty_box","Empty Box")
		self.info_box_stack.add_titled(self.info_box,"infobox","InfoBox")

		self.wawabox2=Gtk.HBox()
		self.wawabox2.pack_start(self.info_box_stack,True,True,0)

		self.apt_box.pack_start(self.wawabox2,False,False,5)


		self.info_box.set_margin_bottom(20)
		self.info_box.set_margin_left(5)
		self.info_box.set_margin_right(5)

		self.info_box_stack.set_visible_child_name("empty_box")
				
		
	#def __init__
	
	


	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("first-aid-kit.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		
		self.separator4.set_name("SEPARATOR_MAIN")
		self.info_box.set_name("PKG_BOX")
		self.apt_execute_button.set_name("EXECUTE_BUTTON")
		self.apt_box7.set_name("PKG_BOX")
		self.apt_txt.set_name("OPTION_LABEL")
		self.apt_label.set_name("SECTION_LABEL")
		self.txt_check_apt.set_name("INFO_LABEL")
			
	#def set-css_info





	def connect_signals(self):
		
		self.apt_execute_button.connect("clicked",self.apt_execute_button_clicked)
		
	#def connect_signals





	def apt_execute_button_clicked(self,widget):
		
		self.thread=threading.Thread(target=self.apt_execute_button_thread)
		self.apt_execute_button.set_sensitive(False)
		self.thread.daemon=True
		self.thread.start()
		
		allocation=self.apt_execute_button.get_allocation()
		w=allocation.width
		h=allocation.height

		self.apt_execute_button.hide()
		self.apt_spinner.start()
		self.apt_spinner.set_size_request(w,h)
		self.apt_spinner.show()

		self.info_box_stack.set_visible_child_name("infobox")
		self.txt_check_apt.set_text(_("You are modifying the repositories, close the external app when you finished with it."))

		GLib.timeout_add(500,self.check_apt_execute_button_thread)
	
	#apt_execute_button_clicked



	def apt_execute_button_thread(self):
	
		try:
			self.core.working=True
			self.core.dprint("Modifying repositories.........","[AptBox]")
			os.system('lliurex-apt2')
			self.thread_ret={"status":True,"msg":"BROKEN"}
			
		except Exception as e:
			self.core.dprint("(apt_execute_button_thread)Error: %s"%e,"[AptBox]")
			return False
			
	#def apt_execute_button_thread


	def check_apt_execute_button_thread(self):
		
		if self.thread.is_alive():
			return True
		
		self.core.working=False

		self.apt_spinner.hide()
		self.apt_execute_button.show()
		self.apt_execute_button.set_sensitive(True)
		self.info_box_stack.set_visible_child_name("empty_box")
		self.info_box_stack.set_visible_child_name("infobox")
		self.txt_check_apt.set_text(_("You have mofified the repositories."))
		self.core.dprint("You have mofified the repositories...FINISHED!!","[AptBox]")
		
	#check_apt_execute_button_thread
