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

gettext.textdomain('first-aid-kit-gui')
_=gettext.gettext


RSRC="./rsrc/"


class StartBarBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('first-aid-kit-gui')
		ui_path=RSRC + "first-aid-kit.ui"
		builder.add_from_file(ui_path)
		
		
		self.start_bar_box=builder.get_object("start_bar_box")
		self.start_bar_box2=builder.get_object("box2")
		self.start_bar_button=builder.get_object("start_bar_button")
		self.start_bar_button_box=builder.get_object("start_bar_button_box")
		self.start_bar_spinner=builder.get_object("start_bar_spinner")
		self.txt_check_start_bar=builder.get_object("txt_check_start_bar")
		self.spinner_start_bar=builder.get_object("spinner_start_bar")
		self.section_label_4=builder.get_object("section_label_4")
		self.label1=builder.get_object("label1")
		self.info_box=builder.get_object("info_start_bar")
		self.info_box_into=builder.get_object("box15")
		self.separator1=builder.get_object("separator1")

		self.add(self.start_bar_box)
		
		self.connect_signals()
		self.set_css_info()

		self.info_box_stack=Gtk.Stack()
		self.info_box_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.info_box_stack.set_transition_duration(500)
		hbox_epoptes=Gtk.HBox()
		hbox_epoptes.show()
		self.info_box_stack.add_titled(hbox_epoptes,"empty_box_start_bar","Empty Box Start Bar")
		self.info_box_stack.add_titled(self.info_box,"info_start_bar","InfoBoxStartBar")

		self.wawabox3=Gtk.HBox()
		self.wawabox3.pack_start(self.info_box_stack,True,True,0)

		self.start_bar_box.pack_start(self.wawabox3,False,False,5)


		self.info_box.set_margin_bottom(20)
		self.info_box.set_margin_left(5)
		self.info_box.set_margin_right(5)

		self.info_box_stack.set_visible_child_name("empty_box_start_bar")

		self.grub_file='/etc/default/grub.d/06-lliurex-cmdline.cfg'
		self.word = 'splash '
		f = open(self.grub_file,'r')
		for line in f:
			if self.word in line:
				self.splash_delete=False
				self.start_bar_button.set_label(_("Delete Startup Bar"))
				self.info_box_stack.set_visible_child_name("empty_box_start_bar")
			else:
				self.splash_delete=True
				self.start_bar_button.set_label(_("Add Startup Bar"))
				self.info_box_stack.set_visible_child_name("empty_box_start_bar")
		f.close()	
		
	#def __init__
	




	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("first-aid-kit.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		
		self.start_bar_button.set_name("EXECUTE_BUTTON")
		self.start_bar_box2.set_name("PKG_BOX")
		self.info_box.set_name("PKG_BOX")
		self.separator1.set_name("SEPARATOR_MAIN")

		self.section_label_4.set_name("SECTION_LABEL")
		self.label1.set_name("OPTION_LABEL")
		self.txt_check_start_bar.set_name("INFO_LABEL")
			
	#def set-css_info



	def connect_signals(self):
		
		self.start_bar_button.connect("clicked",self.start_bar_button_clicked)
		
	#def connect_signals





	def start_bar_button_clicked(self,widget):
		
		self.thread=threading.Thread(target=self.start_bar_button_thread)
		self.start_bar_button.set_sensitive(False)
		self.thread.daemon=True
		self.thread.start()
		
		allocation=self.start_bar_button.get_allocation()
		w=allocation.width
		h=allocation.height

		self.start_bar_button.hide()
		self.start_bar_spinner.start()
		self.start_bar_spinner.set_size_request(w,h)
		self.start_bar_spinner.show()

		GLib.timeout_add(500,self.check_start_bar_thread)
	
	#def_gparted_button_clicked



	def start_bar_button_thread(self):
	
		try:
			
			self.core.working=True
			
			if self.splash_delete == False:
				self.core.dprint("The startup bar has been removed from your system.","[StarBarBox]")
				f = open(self.grub_file,'r')
				lst = []
				for line in f:
					if self.word in line:
						line = line.replace(self.word,'')
					lst.append(line)
				f.close()
				f = open(self.grub_file,'w')
				for line in lst:
					f.write(line)
				f.close()
				self.splash_delete = True
				self.start_bar_button.set_label(_("Add Startup Bar"))
				self.info_box_stack.set_visible_child_name("info_start_bar")
				self.txt_check_start_bar.set_text(_("The startup bar is removing from your system, applying changes....."))
			else:
				self.core.dprint("The startup bar has been added at your system.","[StarBarBox]")
				f = open(self.grub_file,'r')
				lst = []
				match='quiet'
				replace='quiet splash'
				for line in f:
					if match in line:
						line = line.replace(match,replace)
					lst.append(line)
				f.close()
				f = open(self.grub_file,'w')
				for line in lst:
					f.write(line)
				f.close()
				self.splash_delete = False
				self.start_bar_button.set_label(_("Delete Startup Bar"))
				self.info_box_stack.set_visible_child_name("info_start_bar")
				self.txt_check_start_bar.set_text(_("The startup bar is adding at your system, applying changes....."))

			os.system('update-grub')
			time.sleep(1)
			self.thread_ret={"status":True,"msg":"BROKEN"}
			
		except Exception as e:
			self.core.dprint("(start_bar_button_thread)Error: %s"%e,"[StarBarBox]")
			return False
			
	#def gparted_button_thread


	def check_start_bar_thread(self):
		
		if self.thread.is_alive():
			return True
		
		self.core.working=False
		self.start_bar_spinner.hide()
		self.start_bar_button.show()
		self.start_bar_button.set_sensitive(True)
		self.info_box_stack.set_visible_child_name("empty_box_start_bar")
		
	#check_gparted_thread