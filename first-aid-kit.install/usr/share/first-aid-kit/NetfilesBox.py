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
import xmlrpclib
import datetime
from dateutil import parser

gettext.textdomain('first-aid-kit')
_=gettext.gettext


RSRC="./rsrc/"


class NetfilesBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('first-aid-kit')
		ui_path=RSRC + "first-aid-kit.ui"
		builder.add_from_file(ui_path)
		self.acl_time_path="/tmp/.fak_acl_timepath"
		
		
		self.netfiles_box=builder.get_object("netfiles_box")
		self.acl_box=builder.get_object("acl_box")
		self.acl_button=builder.get_object("acl_button")
		self.acl_spinner=builder.get_object("acl_spinner")
		self.regenerate_button=builder.get_object("regenerate_button")
		self.regenerate_spinner=builder.get_object("regenerate_spinner")
		self.txt_check_netfiles=builder.get_object("txt_check_netfiles")
		self.spinner_netfiles=builder.get_object("spinner_netfiles")
		self.label10=builder.get_object("label10")
		self.label7=builder.get_object("label7")
		self.section_label_1=builder.get_object("section_label_1")
		self.box11=builder.get_object("box11")
		self.separator2=builder.get_object("separator2")

		self.info_netfiles=builder.get_object("info_netfiles")
		self.info_netfiles_into=builder.get_object("info_netfiles_into")
		self.info_netfiles_txt=builder.get_object("info_netfiles_txt")
		self.info_netfiles_spinner=builder.get_object("info_netfiles_spinner")
		

		self.add(self.netfiles_box)
		
		self.info_netfiles_stack=Gtk.Stack()
		self.info_netfiles_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.info_netfiles_stack.set_transition_duration(500)
		hbox=Gtk.HBox()
		hbox.show()
		self.info_netfiles_stack.add_titled(hbox,"empty_box_netfiles","Empty Box")
		self.info_netfiles_stack.add_titled(self.info_netfiles,"info_netfiles","InfoNetfiles")

		self.wawabox=Gtk.HBox()
		self.wawabox.pack_start(self.info_netfiles_stack,True,True,0)

		self.netfiles_box.pack_start(self.wawabox,False,False,5)


		self.info_netfiles.set_margin_bottom(20)
		self.info_netfiles.set_margin_left(5)
		self.info_netfiles.set_margin_right(5)

		self.info_netfiles_stack.set_visible_child_name("empty_box_netfiles")
		self.acl_executed=False
		self.regenerate_executed=False

		proxy="https://localhost:9779"
		self.client=xmlrpclib.ServerProxy(proxy)

		self.acl_error=[False,"True"]
		self.regenerate_error=[False,"True"]
		
		self.connect_signals()
		self.set_css_info()


	#def __init__
	

	def check_thread_on_startup(self):

		try:
			#thread is alive, because was started before.....
			if self.client.is_acl_thread_alive(self.core.n4d_key,"NetFoldersManager"):
				self.regenerate_button.set_sensitive(False)
				self.acl_button.set_sensitive(False)
				
				if os.path.isfile(self.acl_time_path):
					f=open(self.acl_time_path)
					line=f.readline()
					f.close()
					self.acl_time_start=parser.parse(line)

				else:
					self.acl_time_start=datetime.datetime.now()

				allocation=self.acl_button.get_allocation()
				w=allocation.width
				h=allocation.height

				self.acl_button.hide()
				self.acl_spinner.start()
				self.acl_spinner.set_size_request(w,h)
				self.acl_spinner.show()
				self.info_netfiles_stack.set_visible_child_name("info_netfiles")
				self.acl_elapsed=datetime.datetime.now() - self.acl_time_start
				self.acl_elapsed=self.time_formated(self.acl_elapsed)
				self.info_netfiles_txt.set_text(_("ACLs are still regenerating, time elapsed: %s "%self.acl_elapsed))
				self.core.dprint("ACLs are still regenerating, time elapsed: %s "%self.acl_elapsed)
				GLib.timeout_add(10000,self.check_acl_thread)
		except Exception as e:
			self.core.dprint("(check_thread_on_startup)Error: %s"%e,"[NetfilesBox]")

	#def check_thread


	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("first-aid-kit.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		
		self.box11.set_name("PKG_BOX")
		self.acl_button.set_name("EXECUTE_BUTTON")
		self.regenerate_button.set_name("EXECUTE_BUTTON")
		self.label10.set_name("OPTION_LABEL")
		self.label7.set_name("OPTION_LABEL")
		self.section_label_1.set_name("SECTION_LABEL")
		self.separator2.set_name("SEPARATOR_MAIN")

		self.info_netfiles_txt.set_name("INFO_LABEL")
		self.info_netfiles.set_name("PKG_BOX")
			
	#def set-css_info






	def connect_signals(self):
		
		self.acl_button.connect("clicked",self.acl_button_clicked)
		self.regenerate_button.connect("clicked",self.regenerate_button_clicked)
		
	#def connect_signals





	def acl_button_clicked(self,widget):

		self.thread=threading.Thread(target=self.acl_button_thread)
		self.regenerate_button.set_sensitive(False)
		self.acl_button.set_sensitive(False)
		self.info_netfiles_stack.set_visible_child_name("empty_box_netfiles")
		self.thread.daemon=True
		self.thread.start()
		
		allocation=self.acl_button.get_allocation()
		w=allocation.width
		h=allocation.height

		self.acl_button.hide()
		self.acl_spinner.start()
		self.acl_spinner.set_size_request(w,h)
		self.acl_spinner.show()
		self.info_netfiles_stack.set_visible_child_name("info_netfiles")

		self.acl_time_start=datetime.datetime.now()

		if os.path.isfile(self.acl_time_path):
			os.remove(self.acl_time_path)
		f=open(self.acl_time_path,'w')
		f.write(self.acl_time_start.ctime())
		f.close()

		self.info_netfiles_txt.set_text(_("ACLs are still regenerating...... please, wait."))

		GLib.timeout_add(10000,self.check_acl_thread)
	
	#def acl_button_clicked






	def acl_button_thread(self):
	
		try:
			self.core.working=True
			self.core.dprint("ACL regenerating in /net....","[NetfilesBox]")

			self.client.restore_acls_via_thread(self.core.n4d_key,"NetFoldersManager")

			self.thread_ret={"status":True,"msg":"BROKEN"}
			
		except Exception as e:
			self.core.dprint("(acl_button_thread)Error: %s"%e,"[NetfilesBox]")
			return False
			
	#def acl_button_thread






	def check_acl_thread(self):
		
		try:
			
			if self.client.is_acl_thread_alive(self.core.n4d_key,"NetFoldersManager"):
				self.acl_elapsed=datetime.datetime.now() - self.acl_time_start
				self.acl_elapsed=self.time_formated(self.acl_elapsed)
				self.info_netfiles_txt.set_text(_("ACLs are still regenerating, time elapsed: %s "%self.acl_elapsed))
				self.core.dprint("ACLs are still regenerating, time elapsed %s "%self.acl_elapsed,"[NetfilesBox]")

				return True

			self.core.dprint("ACLs have been regenerated.","[NetfilesBox]")
			self.core.working=False

			self.acl_elapsed=datetime.datetime.now() - self.acl_time_start
			self.acl_elapsed=self.time_formated(self.acl_elapsed)
			self.acl_spinner.hide()
			self.acl_button.show()
			self.regenerate_button.set_sensitive(True)
			self.acl_button.set_sensitive(True)
			self.acl_error=[False,"Perfect"]

			self.acl_executed=True
			self.show_info()

		except Exception as e:
			self.core.dprint("ACL check thread execution Exception: %s"%e,"[NetfilesBox]")
			self.acl_spinner.hide()
			self.acl_button.show()
			self.regenerate_button.set_sensitive(True)
			self.acl_button.set_sensitive(True)
			self.acl_error=[True,e]
			return False
		
	#check_acl_thread







	def regenerate_button_clicked(self,widget):
		
		self.thread=threading.Thread(target=self.regenerate_button_thread)
		self.regenerate_button.set_sensitive(False)
		self.acl_button.set_sensitive(False)
		self.info_netfiles_stack.set_visible_child_name("empty_box_netfiles")
		self.thread.daemon=True
		self.thread.start()
		
		allocation=self.regenerate_button.get_allocation()
		w=allocation.width
		h=allocation.height

		self.regenerate_button.hide()
		self.regenerate_spinner.start()
		self.regenerate_spinner.set_size_request(w,h)
		self.regenerate_spinner.show()
		self.info_netfiles_stack.set_visible_child_name("info_netfiles")
		self.regenerate_time_start=datetime.datetime.now()
		self.info_netfiles_txt.set_text(_("User folders are still regenerating...... please, wait."))

		GLib.timeout_add(500,self.check_regenerate_thread)
	
	#def_regenerate_button_clicked






	def regenerate_button_thread(self):
	
		try:
			self.core.dprint("Regenerating folders /net....","[NetfilesBox]")
			self.core.working=True

			users=self.client.light_get_user_list(self.core.n4d_key,"Golem")
			for user in users:
				user_properties={}
				user_properties["profile"]=user[5]
				user_properties["uid"]=user[1]
				user_properties["uidNumber"]=user[2]
				self.core.dprint("User: %s"%user,"[NetfilesBox]")
				self.core.dprint("user_properties: %s"%user_properties,"[NetfilesBox]")
				self.core.dprint("Testing folders in /net, N4D service.....","[NetfilesBox]")
				self.client.exist_home_or_create(self.core.n4d_key,"Golem",user_properties)

			self.core.dprint("Restore GROUP folders /net, N4D service.....","[NetfilesBox]")
			self.client.restore_groups_folders(self.core.n4d_key,"Golem")
			self.core.dprint("End of all process","[NetfilesBox]")

			self.thread_ret={"status":True,"msg":"BROKEN"}
			
		except Exception as e:
			self.core.dprint("(regenerate_button_thread)Error: %s"%e,"[NetfilesBox]")
			return False
			
	#def regenerate_button_thread







	def check_regenerate_thread(self):
		
		try:
			if self.thread.is_alive():
				self.regenerate_elapsed=datetime.datetime.now() - self.regenerate_time_start
				self.regenerate_elapsed=self.time_formated(self.regenerate_elapsed)
				self.info_netfiles_txt.set_text(_("User folders are still regenerating, time elapsed: %s "%self.regenerate_elapsed))
				self.core.dprint("User folders are still regenerating, time elapsed: %s "%self.regenerate_elapsed,"[NetfilesBox]")
				return True

			self.core.working=False
			
			self.regenerate_elapsed=datetime.datetime.now() - self.regenerate_time_start
			self.regenerate_elapsed=self.time_formated(self.regenerate_elapsed)
			self.regenerate_spinner.hide()
			self.regenerate_button.show()
			self.regenerate_button.set_sensitive(True)
			self.acl_button.set_sensitive(True)

			self.regenerate_executed=True
			self.show_info()

		except Exception as e:
			self.core.dprint("(check_regenerate_thread)Error: %s"%e,"[NetfilesBox]")
			self.regenerate_spinner.hide()
			self.regenerate_button.show()
			self.regenerate_button.set_sensitive(True)
			self.acl_button.set_sensitive(True)
			self.regenerate_error=[True,e]
			return False
		
	#check_regenerate_thread







	def show_info(self):

		if self.acl_error[0]== True:
			self.info_netfiles_stack.set_visible_child_name("info_netfiles")
			self.info_netfiles_txt.set_text(_("ACLs error: %s")%self.acl_error[1])
			if self.regenerate_error[0]==True:
				self.info_netfiles_stack.set_visible_child_name("info_netfiles")
				self.info_netfiles_txt.set_text(_("ACLs error: %s\nRegenerate error:%s")%(self.acl_error[1],self.regenerate_error[1]))
			return True
		if self.regenerate_error[0]==True:
			self.info_netfiles_stack.set_visible_child_name("info_netfiles")
			self.info_netfiles_txt.set_text(_("Regenerate error:%s")%self.regenerate_error[1])
			return True

		if self.acl_executed == True:
			if self.regenerate_executed == False:
				self.info_netfiles_stack.set_visible_child_name("info_netfiles")
				self.info_netfiles_txt.set_text(_("Finished!!!\nACLs of the files have been reviewed. Time elapsed to do %s"%self.acl_elapsed))
			else:
				self.info_netfiles_stack.set_visible_child_name("info_netfiles")
				self.info_netfiles_txt.set_text(_("Finished!!!\nACLs of the files have been reviewed, in %s.\nAll user folders have been regenerated if it's necessary in %s"%(self.acl_elapsed,self.regenerate_elapsed)))
		else:
			if self.regenerate_executed == True:
				self.info_netfiles_stack.set_visible_child_name("info_netfiles")
				self.info_netfiles_txt.set_text(_("Finished!!!\nAll user folders have been regenerated if it's necessary. Time elapsed to do %s")%self.regenerate_elapsed)

	#def show_info






	def time_formated(self,time_timedelta):
		try:

			hours=time_timedelta.seconds//3600
			minutes=time_timedelta.seconds//60
			seconds=time_timedelta.seconds-(minutes*60)

			if hours == 0:
				if minutes == 0:
					return("%s seconds"%seconds)
				else:
					if seconds == 0:
						return("%s min"%minutes)
					else:
						if seconds<10:
							return("%s:%02d min"%(minutes,seconds))
						else:
							return("%s:%s min"%(minutes,seconds))
			else:
				if minutes<10:
					if seconds<10:
						return("%s hours and %02d:%02d minutes"%(hours,minutes,seconds))
					else:
						return("%s hours and %02d:%s minutes"%(hours,minutes,seconds))
				else:
					if seconds<10:
						return("%s hours and %0s:%02d minutes"%(hours,minutes,seconds))
					else:
						return("%s hours and %0s:%s minutes"%(hours,minutes,seconds))

		except Exception as e:
			self.core.dprint("(time_formated)Error: %s"%e,"[NetfilesBox]")

	#def time_formated
