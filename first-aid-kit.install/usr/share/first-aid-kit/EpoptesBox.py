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

gettext.textdomain('first-aid-kit')
_=gettext.gettext


RSRC="./rsrc/"


class EpoptesBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('first-aid-kit')
		ui_path=RSRC + "first-aid-kit.ui"
		builder.add_from_file(ui_path)
		
		
		self.epoptes_box=builder.get_object("epoptes_box")
		self.epoptes_box3=builder.get_object("box3")
		self.renew_button=builder.get_object("renew_button")
		self.renew_spinner=builder.get_object("renew_spinner")
		self.txt_check_epoptes=builder.get_object("txt_check_epoptes")
		self.spinner_netfiles=builder.get_object("spinner_epoptes")
		self.section_label_3=builder.get_object("section_label_3")
		self.label3=builder.get_object("label3")
		self.info_box=builder.get_object("info_epoptes")
		self.info_box_into=builder.get_object("box23")
		self.separator9=builder.get_object("separator9")

		self.add(self.epoptes_box)
		
		self.connect_signals()
		self.set_css_info()

		
		self.info_box_stack=Gtk.Stack()
		self.info_box_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.info_box_stack.set_transition_duration(500)
		hbox_epoptes=Gtk.HBox()
		hbox_epoptes.show()
		self.info_box_stack.add_titled(hbox_epoptes,"empty_box_epoptes","Empty Box Epoptes")
		self.info_box_stack.add_titled(self.info_box,"infobox","InfoBox")

		self.wawabox2=Gtk.HBox()
		self.wawabox2.pack_start(self.info_box_stack,True,True,0)

		self.epoptes_box.pack_start(self.wawabox2,False,False,5)


		self.info_box.set_margin_bottom(20)
		self.info_box.set_margin_left(5)
		self.info_box.set_margin_right(5)

		self.info_box_stack.set_visible_child_name("empty_box_epoptes")
				
		
	#def __init__
	
	


	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("first-aid-kit.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		
		self.renew_button.set_name("EXECUTE_BUTTON")
		self.epoptes_box3.set_name("PKG_BOX")
		self.info_box.set_name("PKG_BOX")
		self.separator9.set_name("SEPARATOR_MAIN")

		self.label3.set_name("OPTION_LABEL")
		self.txt_check_epoptes.set_name("INFO_LABEL")
		self.section_label_3.set_name("SECTION_LABEL")
			
	#def set-css_info





	def connect_signals(self):
		
		self.renew_button.connect("clicked",self.renew_button_clicked)
		
	#def connect_signals





	def renew_button_clicked(self,widget):
		
		self.thread=threading.Thread(target=self.renew_button_thread)
		self.renew_button.set_sensitive(False)
		self.thread.daemon=True
		self.thread.start()
		
		allocation=self.renew_button.get_allocation()
		w=allocation.width
		h=allocation.height

		self.renew_button.hide()
		self.renew_spinner.start()
		self.renew_spinner.set_size_request(w,h)
		self.renew_spinner.show()

		GLib.timeout_add(500,self.check_renew_thread)
	
	#def_gparted_button_clicked



	def renew_button_thread(self):
	
		try:
			self.core.working=True
			self.core.dprint("renewing the certificate of the epoptes....","[StarBarBox]")
			os.system('epoptes-client -c')
			time.sleep(1)
			self.thread_ret={"status":True,"msg":"BROKEN"}
			
		except Exception as e:
			self.core.dprint("(renew_button_thread)Error: %s"%e,"[EpoptesBox]")
			return False
			
	#def gparted_button_thread


	def check_renew_thread(self):
		
		if self.thread.is_alive():
			return True
		
		self.core.working=False

		self.renew_spinner.hide()
		self.renew_button.show()
		self.renew_button.set_sensitive(True)
		self.info_box_stack.set_visible_child_name("infobox")
		self.txt_check_epoptes.set_text(_("The Epoptes certificate has been renewed"))
		
	#check_gparted_thread
