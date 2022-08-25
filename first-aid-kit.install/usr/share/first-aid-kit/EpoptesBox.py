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
import netifaces

from n4d.client import Client

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
		self.epoptes_internet_box=builder.get_object("box30")
		self.epotes_internet_msg=builder.get_object("epotes_internet_msg")
		self.epoptes_internet_image=builder.get_object("epoptes_internet_image")
		self.renew_spinner_internet_epoptes=builder.get_object("renew_spinner_internet_epoptes")
		self.renew_button_internet_epoptes=builder.get_object("renew_button_internet_epoptes")
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
		self.renew_button_internet_epoptes.set_name("EXECUTE_BUTTON")
		self.epoptes_box3.set_name("PKG_BOX")
		self.epoptes_internet_box.set_name("PKG_BOX")
		self.info_box.set_name("PKG_BOX")
		self.epotes_internet_msg.set_name("OPTION_LABEL")
		self.separator9.set_name("SEPARATOR_MAIN")

		self.label3.set_name("OPTION_LABEL")
		self.txt_check_epoptes.set_name("INFO_LABEL")
		self.section_label_3.set_name("SECTION_LABEL")
			
	#def set-css_info





	def connect_signals(self):
		
		self.renew_button.connect("clicked",self.renew_button_clicked)
		self.renew_button_internet_epoptes.connect("clicked",self.renew_button_internet_epoptes_clicked)
		
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




	def renew_button_internet_epoptes_clicked(self,widget):
		
		self.info_box_stack.set_visible_child_name("empty_box_epoptes")
		self.thread=threading.Thread(target=self.renew_button_internet_epoptes_thread)
		self.renew_button_internet_epoptes.set_sensitive(False)
		self.thread.daemon=True
		self.thread.start()
		
		allocation=self.renew_button_internet_epoptes.get_allocation()
		w=allocation.width
		h=allocation.height

		self.renew_button_internet_epoptes.hide()
		self.renew_spinner_internet_epoptes.start()
		self.renew_spinner_internet_epoptes.set_size_request(w,h)
		self.renew_spinner_internet_epoptes.show()

		GLib.timeout_add(500,self.check_renew_internet_thread)
	
	#def_renew_button_internet_epoptes_clicked



	def renew_button_internet_epoptes_thread(self):
	
		try:
			self.core.working=True
			self.finded=False
			self.my_interfaces=[]

			self.core.dprint("Testing if my internet in blocked in iptables...","[EpoptesBox]")
			self.n4d_server = "https://server:9779"
			self.n4d_client = Client(self.n4d_server)
			self.list=self.n4d_client.EpoptesServer.list_iptables()
			self.core.dprint("EpoptesServer send: %s"%self.list,"[EpoptesBox]")
			for interface in netifaces.interfaces():
				self.my_interfaces.append((netifaces.ifaddresses(interface)[netifaces.AF_INET])[0]['addr'])
			
			#Si el resultado es True y la lista posee algun valor de ip bloqueada compruebo que no soy yo.
			if self.list[0]:
				#self.core.dprint("Salida true del epoptes server","[EpoptesBox]")
				if self.list[1]:
					#self.core.dprint("La lista no es vacia","[EpoptesBox]")
					for element in self.my_interfaces:
						self.core.dprint("Comprobando la IP: %s."%element,"[EpoptesBox]")
						if self.check_availability(element,self.list[1]):
							self.finded=True
							self.txt_check_epoptes.set_text("My Ip %s address is blocked by Epoptes in iptables list %s"%(element,self.list[1]))
							break
						else:
							self.txt_check_epoptes.set_text("My internet access is not blocked by Epoptes.")
				else:
					self.txt_check_epoptes.set_text('No IP is blocked at the server.')
			else:
				self.txt_check_epoptes.set_text('Any problem to read blocked IP list.')

			time.sleep(1)
			self.thread_ret={"status":True,"msg":"BROKEN"}
			
		except Exception as e:
			self.core.dprint("(renew_button_internet_epoptes_thread)Error: %s"%e,"[EpoptesBox]")
			return False
			
	#def renew_button_internet_epoptes_thread

	


	def check_availability(self,element, collection: iter):
		
		try:
			return element in collection
		except Exception as e:
			self.core.dprint("(check_availability)Error: %s"%e,"[EpoptesBox]")
			return False

	#def check_availability





	def check_renew_internet_thread(self):
		
		if self.thread.is_alive():
			return True
		
		self.core.working=False

		self.renew_spinner_internet_epoptes.hide()
		self.renew_button_internet_epoptes.show()
		self.renew_button_internet_epoptes.set_sensitive(True)
		if self.finded:
			self.core.dprint("My internet access is BLOCKED by Epoptes.","[EpoptesBox]")
			#self.txt_check_epoptes.set_text("My Ip address is blocked in iptables %s"%self.list[1])
			self.epoptes_internet_image.set_from_stock("gtk-no",Gtk.IconSize.BUTTON)
			self.server_connection=False
		else:
			self.core.dprint("My internet access is not blocked by Epoptes.","[EpoptesBox]")
			#self.txt_check_epoptes.set_text("My Ip address can access to internet. %s"%self.list[1])
			self.epoptes_internet_image.set_from_stock("gtk-yes",Gtk.IconSize.BUTTON)
			self.server_connection=True
		self.info_box_stack.set_visible_child_name("infobox")
		#self.txt_check_epoptes.set_text()
		
	#check_renew_internet_thread





