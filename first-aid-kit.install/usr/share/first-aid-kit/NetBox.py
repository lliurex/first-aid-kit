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
import urllib2
import lliurex.net
import subprocess

gettext.textdomain('first-aid-kit')
_=gettext.gettext


RSRC="./rsrc/"


class NetBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('first-aid-kit')
		ui_path=RSRC + "first-aid-kit.ui"
		builder.add_from_file(ui_path)

		
		self.net_box=builder.get_object("net_box")
		self.test_button=builder.get_object("test_button")
		self.test_combobox=builder.get_object("test_combobox")
		self.test_spinner=builder.get_object("test_spinner")
		self.restart_button=builder.get_object("restart_button")
		self.restart_spinner=builder.get_object("restart_spinner")
		self.configure_network_button=builder.get_object("configure_network_button")
		self.configure_network_spinner=builder.get_object("configure_network_spinner")
		self.check4_image=builder.get_object("image7")
		self.check2_image=builder.get_object("image5")
		self.check1_image=builder.get_object("image4")
		

		self.section_label_01=builder.get_object("section_label_01")
		self.label5=builder.get_object("label5")
		self.label2=builder.get_object("label2")
		self.speed_net=builder.get_object("label4")
		self.link_label=builder.get_object("label9")
		self.ip_address_label=builder.get_object("label13")
		self.ip_address=builder.get_object("label14")
		self.label6=builder.get_object("label6")
		self.restart_txt=builder.get_object("restart_txt")
		self.configure_network_txt=builder.get_object("configure_network_txt")
		
		
		self.separator5=builder.get_object("separator5")
		
		self.box1=builder.get_object("box1")
		self.box9=builder.get_object("box9")

		self.info_box=builder.get_object("info_nettest")
		self.info_box_into=builder.get_object("box14")
		self.txt_check_nettest=builder.get_object("txt_check_nettest")
		self.spinner_nettest=builder.get_object("spinner_nettest")


		self.info_box_stack=Gtk.Stack()
		self.info_box_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.info_box_stack.set_transition_duration(500)
		hbox_nettest=Gtk.HBox()
		hbox_nettest.show()
		self.info_box_stack.add_titled(hbox_nettest,"empty_box_start_bar","Empty Box Start Bar")
		self.info_box_stack.add_titled(self.info_box,"infobox","InfoBox")

		self.wawabox3=Gtk.HBox()
		self.wawabox3.pack_start(self.info_box_stack,True,True,0)

		self.net_box.pack_start(self.wawabox3,False,False,5)


		self.info_box.set_margin_bottom(20)
		self.info_box.set_margin_left(5)
		self.info_box.set_margin_right(5)

		self.load_eth_cards()
		self.pack_start(self.net_box,True,True,5)
		self.connect_signals()
		self.set_css_info()

		self.info_box_stack.set_visible_child_name("empty_box_start_bar")
		#self.info_box_stack.set_visible_child_name("infobox")
		#self.txt_check_nettest.set_text(_("Your internet server is down, please review the proxy or the router."))
		
	#def __init__
	




	
	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("first-aid-kit.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		
		self.box1.set_name("PKG_BOX")
		self.box9.set_name("PKG_BOX")
		
		self.test_button.set_name("EXECUTE_BUTTON")
		self.restart_button.set_name("EXECUTE_BUTTON")
		self.configure_network_button.set_name("EXECUTE_BUTTON")
				
		self.section_label_01.set_name("SECTION_LABEL")
		self.label5.set_name("OPTION_LABEL")
		self.label2.set_name("OPTION_LABEL")
		self.speed_net.set_name("OPTION_LABEL")
		self.label6.set_name("OPTION_LABEL")
		self.restart_txt.set_name("OPTION_LABEL")
		self.configure_network_txt.set_name("OPTION_LABEL")
		self.ip_address_label.set_name("OPTION_LABEL")
		self.ip_address.set_name("OPTION_LABEL")
		self.link_label.set_name("OPTION_LABEL")
		self.separator5.set_name("SEPARATOR_MAIN")
		self.txt_check_nettest.set_name("INFO_LABEL")
		self.info_box.set_name("PKG_BOX")
			
	#def set-css_info



	def connect_signals(self):
		
		self.test_combobox.connect("changed",self.eth_changed)
		self.test_button.connect("clicked",self.test_button_clicked)
		self.restart_button.connect("clicked",self.restart_button_clicked)
		self.configure_network_button.connect("clicked",self.configure_network_button_clicked)
		
	#def connect_signals




	def load_eth_cards(self):

		self.eth_store=Gtk.ListStore(str)

		self.devices=lliurex.net.get_devices_info()
		self.num_devices=len(self.devices)
		self.core.dprint("Netcards detected NUMBER: %s"%self.num_devices,"[NetBox]")
		self.eth_wharehouse={}

		if self.num_devices > 1:
			for i in range(0,self.num_devices):
				eth_name=self.devices[i]['name']
				self.eth_store.append([eth_name])
				self.eth_wharehouse[eth_name]=""
				self.eth_wharehouse[eth_name]=i
		else:
			self.test_combobox.hide()

		self.core.dprint("Netcards detected NAME: %s"%self.eth_wharehouse,"[NetBox]")
		renderer=Gtk.CellRendererText()
		self.test_combobox.pack_start(renderer,True)
		self.test_combobox.add_attribute(renderer,"text",0)
		self.test_combobox.set_model(self.eth_store)
		self.test_combobox.set_active(0)
		self.eth_po=0


	#def load_eth



	def eth_changed(self,widget):

		it=self.test_combobox.get_active_iter()
		eth_selected=self.eth_store.get(it,0)[0]
		self.eth_po=self.eth_wharehouse[eth_selected]
		self.core.dprint("Network selected to test: %s  in position: %s"%(eth_selected,self.eth_po),"[NetBox]")
		#RESET ALL VARIABLES IN GUI
		self.info_box_stack.set_visible_child_name("empty_box_start_bar")
		self.check1_image.set_from_stock("gtk-dialog-question",Gtk.IconSize.BUTTON)
		self.check2_image.set_from_stock("gtk-dialog-question",Gtk.IconSize.BUTTON)
		self.check4_image.set_from_stock("gtk-dialog-question",Gtk.IconSize.BUTTON)
		self.speed_net.set_text(_("Unknow"))
		self.ip_address.set_text(_("Unknow"))


	#def eth_changed


	def test_button_clicked(self,widget):
		
		self.thread=threading.Thread(target=self.test_button_thread)
		self.test_button.set_sensitive(False)
		self.info_box_stack.set_visible_child_name("empty_box_start_bar")
		self.thread.daemon=True
		self.thread.start()
		
		allocation=self.test_button.get_allocation()
		w=allocation.width
		h=allocation.height

		self.test_combobox.hide()
		self.test_button.hide()
		self.test_spinner.start()
		self.test_spinner.set_size_request(w,h)
		self.test_spinner.show()

		GLib.timeout_add(500,self.check_test_thread)
	
	#def_test_button_clicked



	def test_button_thread(self):
	
		try:
			self.device_info()
			if self.server_on():
				self.core.dprint("Server connection is avaiable.","[NetBox]")
				self.check1_image.set_from_stock("gtk-yes",Gtk.IconSize.BUTTON)
				self.server_connection=True
			else:
				self.core.dprint("Server connection is UNAVAIABLE....","[NetBox]")
				self.check1_image.set_from_stock("gtk-no",Gtk.IconSize.BUTTON)
				self.server_connection=Falsee

			self.core.dprint("Test Network....","[NetBox]")
			if self.internet_on():
				self.core.dprint("Ping to google is ok....","[NetBox]")
				self.check2_image.set_from_stock("gtk-yes",Gtk.IconSize.BUTTON)
				self.internet_connection=True
			else:
				self.core.dprint("Internet is unavaiable","[NetBox]")
				self.check2_image.set_from_stock("gtk-no",Gtk.IconSize.BUTTON)
				self.internet_connection=False


			self.thread_ret={"status":True,"msg":"BROKEN"}
			
		except Exception as e:
			self.core.dprint("(test_button_thread)Error: %s"%e,"[NetBox]")
			return False
			
	#def Test_button_thread


	def check_test_thread(self):
		
		if self.thread.is_alive():
			return True
		
		
		self.test_spinner.hide()
		self.test_button.show()
		self.test_combobox.show()
		self.test_button.set_sensitive(True)
		self.info_user_test()
		
		
	#check_test_thread



	def server_on(self):
		try:
			import xmlrpclib as x
			proxy="https://server:9779"
			client=x.ServerProxy(proxy)
			client.get_methods()
			return True
		except Exception as e:
			self.core.dprint("(server_on)Error: %s"%e,"[NetBox]")
			return False


	#def_internet_on


	def internet_on(self):
		try:
			urllib2.urlopen('https://www.google.com/', timeout=10)
			return True
		except Exception as e:
			self.core.dprint("(internet_on)Error: %s"%e,"[NetBox]")
			return False


	#def_internet_on

	def device_info(self):
		try:

			self.name_device=self.devices[self.eth_po]['name']
			self.core.dprint ("Device info: %s"%self.name_device,"[NetBox]")
			self.speed_device=self.devices[self.eth_po]['Speed']
			self.link_device=self.devices[self.eth_po]['Link detected']
			self.ip_device=self.devices[self.eth_po]['ip']
			self.core.dprint("Name:%s - Speed:%s - Link:%s - Ip:%s"%(self.name_device,self.speed_device,self.link_device,self.ip_device),"[NetBox]")
			

			if self.speed_device[0] == "":
				self.speed_net.set_text(_("Unknow"))
			else:
				self.speed_net.set_text(self.speed_device[0])


			if self.ip_device == "":
				self.ip_address.set_text(_("Unknow"))
			else:
				self.ip_address.set_text(self.ip_device)


			if self.link_device[0] == 'yes':
				self.check4_image.set_from_stock("gtk-yes",Gtk.IconSize.BUTTON)
				self.link_connection=True
			else:
				self.check4_image.set_from_stock("gtk-no",Gtk.IconSize.BUTTON)
				self.link_connection=False

			self.core.dprint("link_connection: %s"%self.link_connection,"[NetBox]")

		except Exception as e:
			#print(e)
			self.core.dprint("(device_info)Error: %s"%e,"[NetBox]")
			self.link_connection=False
			self.check4_image.set_from_stock("gtk-no",Gtk.IconSize.BUTTON)
			self.speed_net.set_text(_("Unknow"))
			self.ip_address.set_text(_("Unknow"))
			return False


	#def_internet_on









	def configure_network_button_clicked(self,widget):
		
		self.thread=threading.Thread(target=self.configure_network_button_thread)
		self.configure_network_button.set_sensitive(False)
		self.thread.daemon=True
		self.thread.start()
		
		allocation=self.configure_network_button.get_allocation()
		w=allocation.width
		h=allocation.height

		self.configure_network_button.hide()
		self.configure_network_spinner.start()
		self.configure_network_spinner.set_size_request(w,h)
		self.configure_network_spinner.show()

		GLib.timeout_add(500,self.check_configure_network_thread)
	
	#def_configure_network_button_clicked




	def restart_button_clicked(self,widget):
		
		self.thread=threading.Thread(target=self.restart_button_thread)
		self.restart_button.set_sensitive(False)
		self.thread.daemon=True
		self.thread.start()

		self.test_button.set_sensitive(False)
		self.test_combobox.set_sensitive(False)
		self.info_box_stack.set_visible_child_name("empty_box_start_bar")
		
		allocation=self.restart_button.get_allocation()
		w=allocation.width
		h=allocation.height

		self.restart_button.hide()
		self.restart_spinner.start()
		self.restart_spinner.set_size_request(w,h)
		self.restart_spinner.show()

		GLib.timeout_add(500,self.check_restart_thread)
	
	#def_restart_button_clicked



	def restart_button_thread(self):
	
		try:
			self.core.working=True
			self.core.dprint("Restart networking....","[NetBox]")
			#os.system(self.core.restart_net)
			#time.sleep(1)

			proc=subprocess.Popen(self.core.restart_net,shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")

			for line in iter(proc.stderr.readline,""):
				line=line.strip("\n")
				self.core.dprint("(restart_button_thread) Subprocess stdout: %s"%line,"[NetBox]")
				
				#self.core.lprint("(kernel_install_thread) Subprocess stderr: %s"%stderr,"[KernelBox]")
			proc.wait()
			self.core.dprint("Restart networking....FINISHED!!!","[NetBox]")

			self.thread_ret={"status":True,"msg":"BROKEN"}
			
		except Exception as e:
			self.core.dprint("(restart_button_thread)Error: %s"%e,"[NetBox]")
			return False
			
	#def restart_button_thread


	def check_restart_thread(self):
		
		if self.thread.is_alive():
			return True
		
		self.core.working=False
		self.restart_spinner.hide()
		self.restart_button.show()
		self.restart_button.set_sensitive(True)
		self.test_button.set_sensitive(True)
		self.test_combobox.set_sensitive(True)
		self.info_box_stack.set_visible_child_name("infobox")
		self.txt_check_nettest.set_text(_("The network card has been reset"))
		#self.info_box_network_stack.set_visible_child_name("infobox")
		#self.txt_check_network.set_text("The network card has been reset")
		
	#check_restart_thread



	def configure_network_button_clicked(self,widget):
		
		self.thread=threading.Thread(target=self.configure_network_button_thread)
		self.configure_network_button.set_sensitive(False)
		self.thread.daemon=True
		self.thread.start()
		
		allocation=self.configure_network_button.get_allocation()
		w=allocation.width
		h=allocation.height

		self.configure_network_button.hide()
		self.configure_network_spinner.start()
		self.configure_network_spinner.set_size_request(w,h)
		self.configure_network_spinner.show()

		GLib.timeout_add(500,self.check_configure_network_thread)
	
	#def_configure_network_button_clicked



	def configure_network_button_thread(self):
	
		try:
			self.core.working=True
			self.core.dprint("Configure network....","[NetBox]")
			#os.system('epoptes-client -c')
			time.sleep(1)
			self.thread_ret={"status":True,"msg":"BROKEN"}
			
		except Exception as e:
			self.core.dprint("(configure_network_button_thread)Error: %s"%e,"[NetBox]")
			return False
			
	#def configure_network_button_thread


	def check_configure_network_thread(self):
		
		if self.thread.is_alive():
			return True
		
		self.core.working=False
		self.configure_network_spinner.hide()
		self.configure_network_button.show()
		self.configure_network_button.set_sensitive(True)
		#self.info_box_network_stack.set_visible_child_name("infobox")
		#self.txt_check_network.set_text("The network card has been reset")
		
	#check_configure_network_thread


	def info_user_test(self):

		try:
			if self.link_connection==False:

				self.info_box_stack.set_visible_child_name("infobox")
				self.txt_check_nettest.set_text(_("You have hardware problems, please review your data\n cable and your connections, because your netcard doesn't have link."))

			else:

				if self.server_connection==False:

					self.info_box_stack.set_visible_child_name("infobox")
					self.txt_check_nettest.set_text(_("You can't connect with server, are you sure that\n the server is started? Please review it and reboot your sistem."))

				else:

					if self.internet_connection==False:

						self.info_box_stack.set_visible_child_name("infobox")
						self.txt_check_nettest.set_text(_("Your internet server is down,\n please review the internet server connection, the proxy or the router."))

			return True
		
		except Exception as e:

			self.core.dprint("(info_user_test)Error: %s"%e,"[NetBox]")
			return False

	#def info_user_test
	
