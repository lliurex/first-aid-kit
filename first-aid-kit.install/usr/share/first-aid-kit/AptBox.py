import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

import copy
import gettext
import Core
#import InformationBox

#import Dialog
import time
import threading
import sys
import os
import subprocess
import time
import datetime

gettext.textdomain('first-aid-kit')
_=gettext.gettext


RSRC="./rsrc/"


class AptBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('first-aid-kit')
		ui_path=RSRC + "first-aid-kit.ui"
		builder.add_from_file(ui_path)
		
		
		self.apt_box=builder.get_object("apt_box")
		self.apt_box7=builder.get_object("box7")
		self.apt_execute_button=builder.get_object("apt_execute_button")
		self.apt_spinner=builder.get_object("apt_spinner")
		self.apt_txt=builder.get_object("apt_txt")

		self.apt_box26=builder.get_object("box26")
		self.apt_pinning_switch=builder.get_object("pinning_switch")
		self.apt_pinning_spinner=builder.get_object("pinning_spinner")
		self.apt_pinning_txt=builder.get_object("pinning_txt")
		self.apt_pinning_detected=builder.get_object("pinning_detected")
		
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

		try:
			if self.core.pinning():
				self.apt_pinning_detected.set_text(_('Active'))
				self.apt_pinning_switch.set_active(True)
				
			else:
				self.apt_pinning_detected.set_text(_('Removed'))
				self.apt_pinning_switch.set_active(False)
				self.apt_pinning_detected.set_name("INFO_LABEL_ERROR")

		except Exception as e:
			self.core.dprint("(INIT)Error pinning detection: %s"%e,"[AptBox]")
			self.apt_pinning_detected.set_text(_('Unknow'))	
				
		
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
		self.apt_box26.set_name("PKG_BOX")
		self.apt_pinning_txt.set_name("OPTION_LABEL")
		self.apt_pinning_detected.set_name("OPTION_LABEL")
		self.apt_label.set_name("SECTION_LABEL")
		self.txt_check_apt.set_name("INFO_LABEL")
			
	#def set-css_info





	def connect_signals(self):
		
		self.apt_execute_button.connect("clicked",self.apt_execute_button_clicked)
		self.apt_pinning_switch.connect("notify::active",self.apt_pinning_switched)
		
	#def connect_signals

	def apt_pinning_switched(self,widget,params):

		try:

			self.file_pinning_rsrc="/usr/share/first-aid-kit/rsrc/lliurex-pinning"
			self.file_pinning_apt="/etc/apt/preferences.d/lliurex-pinning"
			self.file_pinning_restore_rsrc="/usr/share/first-aid-kit/rsrc/lliurex-pinning_restore"
			self.file_pinning_restore_n4d="/etc/n4d/one-shot/lliurex-pinning_restore"
			self.cronfile="/etc/crontab"

			if self.apt_pinning_switch.get_state():
				# Pinning is actived, update information in GUI and deleting a task to restart the pinning file.
				pinning=_('Active')
				self.apt_pinning_detected.set_text(pinning)
				label_pinning=""
				os.system('cp %s %s'%(self.file_pinning_rsrc,self.file_pinning_apt))
				if os.path.isfile(self.file_pinning_restore_n4d):
					os.system('rm %s'%self.file_pinning_restore_n4d)
				self.pinning_cron_deleting()

			else:
				# Pinning is removed, update information in GUI and programing a task to restart the pinning file
				pinning=_('Removed')
				self.apt_pinning_detected.set_text(pinning)
				self.core.dprint("(apt_pinning_switched) Pinning removed, be careful","[AptBox]")
				os.remove(self.file_pinning_apt)
				label_pinning="INFO_LABEL_ERROR"
				os.system('cp %s %s'%(self.file_pinning_restore_rsrc,self.file_pinning_restore_n4d))
				os.system('chmod +x %s'%self.file_pinning_restore_n4d)
				self.pinning_cron_restoring()

			#object in Information GUI view.
			pinning_tex_information=self.core.information_box.information_box.get_children()[2].get_children()[0].get_children()[1].get_children()[0].get_children()[0]
			#print (pinning_tex_information)

			self.apt_pinning_detected.set_text(pinning)
			self.apt_pinning_detected.set_name(label_pinning)
			pinning_tex_information.set_text(pinning)
			pinning_tex_information.set_name(label_pinning)

		except Exception as e:
			self.core.dprint("(apt_pinning_switched)Error pinning switching: %s"%e,"[AptBox]")

	#def apt_pinning_switched



	def pinning_cron_restoring(self):

		try:

			#Set one hour later
			time_now = datetime.datetime.now()
			hour_later=datetime.timedelta(hours=1)
			#hour_later=datetime.timedelta(minutes=2)
			time_later=time_now+hour_later
			hour_cron=str(time_later.hour)
			minute_cron=str(time_later.minute)

			newcron_string = minute_cron+" "+hour_cron+" "+"* * *	root	%s"%self.file_pinning_restore_n4d
			opened_file = open(self.cronfile, 'a')
			opened_file.write("%s\n"%newcron_string)
			opened_file.close()

		except Exception as e:
			self.core.dprint("(pinning_restoring)Error pinning switching: %s"%e,"[AptBox]")

	#def pinning_restoring


	def pinning_cron_deleting(self):
		try:
			f = open(self.cronfile)
			output = []
			for line in f:
				if not "lliurex-pinning" in line:
					output.append(line)
			f.close()
			f = open(self.cronfile, 'w')
			f.writelines(output)
			f.close()

		except Exception as e:
			print("[AptBox](pinning_cron_deleting)Error pinning deleting: %s"%e)

	#def pinning_cron_deleting





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
		self.txt_check_apt.set_name("INFO_LABEL")
		self.txt_check_apt.set_text(_("You are modifying the repositories, close the external app when you finished with it."))

		GLib.timeout_add(500,self.check_apt_execute_button_thread)
	
	#apt_execute_button_clicked



	def apt_execute_button_thread(self):
	
		try:
			self.core.working=True
			self.core.dprint("Modifying repositories.........","[AptBox]")
			proc=subprocess.Popen('repoman',shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
			output,error=proc.communicate()

			if not '/bin/bash' in  error:
				self.error=False
			else:
				self.info_box_stack.set_visible_child_name("infobox")
				self.txt_check_apt.set_name("INFO_LABEL_ERROR")
				self.txt_check_apt.set_text(_("Sorry but the app to modify the repositories can't be opened"))
				self.error=True
				
		except subprocess.CalledProcessError as e:
			self.core.dprint("(apt_execute_button_thread)Error: %s"%e,"[AptBox]")
			self.info_box_stack.set_visible_child_name("infobox")
			self.txt_check_apt.set_name("INFO_LABEL_ERROR")
			self.txt_check_apt.set_text(_("Sorry but the app to modify the repositories can't be opened"))
			self.error=True
			return False
			
	#def apt_execute_button_thread


	def check_apt_execute_button_thread(self):
		
		if self.thread.is_alive():
			return True
		
		self.core.working=False

		self.apt_spinner.hide()
		self.apt_execute_button.show()
		self.apt_execute_button.set_sensitive(True)
		if not self.error:
			self.info_box_stack.set_visible_child_name("empty_box")
			self.info_box_stack.set_visible_child_name("infobox")
			self.txt_check_apt.set_name("INFO_LABEL")
			self.txt_check_apt.set_text(_("You have mofified the repositories."))
			self.core.dprint("You have mofified the repositories...FINISHED!!","[AptBox]")
		
	#check_apt_execute_button_thread
