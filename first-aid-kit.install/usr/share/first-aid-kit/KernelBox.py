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
import subprocess
import apt
import platform
import copy
import shutil

gettext.textdomain('first-aid-kit')
_=gettext.gettext


RSRC="./rsrc/"


class KernelBox(Gtk.VBox):
	
	
	def __init__(self):
		
		try:
			Gtk.VBox.__init__(self)
		
			self.core=Core.Core.get_core()
			
			builder=Gtk.Builder()
			builder.set_translation_domain('first-aid-kit')
			ui_path=RSRC + "first-aid-kit.ui"
			builder.add_from_file(ui_path)
			
			
			self.kernel_box=builder.get_object("kernel_box")
			self.kernel_label=builder.get_object("kernel_label")
			self.kernel_vp=builder.get_object("viewport3")
			self.kernel_sw=builder.get_object("scrolledwindow4")
			self.info_box_kernel=builder.get_object("info_kernel")
			self.txt_check_kernel=builder.get_object("txt_check_kernel")
			self.spinner_info_kernel=builder.get_object("spinner_info_kernel")
			self.separator_kernel=builder.get_object("separator3")
			self.kernel_list_box=builder.get_object("box16")
			self.entry_kernel=builder.get_object("entry_kernel")
			self.update_kernels_button=builder.get_object("kernel_update_button")
			self.filter_kernels_button=builder.get_object("kernel_filter_button")
			self.apply_kernel_button=builder.get_object("apply_kernel_button")
			self.kernel_combobox=builder.get_object("kernel_combobox")
			self.kernel_combobox_spinner=builder.get_object("kernel_combobox_spinner")
			self.switch_kernel_installed=builder.get_object("switch_kernel_installed")
			self.kernel_installed_spinner=builder.get_object("kernel_installed_spinner")
			

			self.add(self.kernel_box)
			
			


			self.info_box_stack=Gtk.Stack()
			self.info_box_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
			self.info_box_stack.set_transition_duration(500)
			hbox_kernel=Gtk.HBox()
			hbox_kernel.show()
			self.info_box_stack.add_titled(hbox_kernel,"empty_box_kernel","Empty Box Kernel")
			self.info_box_stack.add_titled(self.info_box_kernel,"info_kernel","InfoBoxKernel")

			self.wawabox3=Gtk.HBox()
			self.wawabox3.pack_start(self.info_box_stack,True,True,0)

			self.kernel_box.pack_start(self.wawabox3,False,False,5)


			self.info_box_kernel.set_margin_bottom(20)
			self.info_box_kernel.set_margin_left(5)
			self.info_box_kernel.set_margin_right(5)

			self.info_box_stack.set_visible_child_name("empty_box_kernel")


			self.kernel_box_stack=Gtk.Stack()
			self.kernel_box_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
			self.kernel_box_stack.set_transition_duration(500)
			load_spinner=Gtk.Spinner()
			load_spinner.show()
			load_spinner.start()
			self.kernel_box_stack.add_titled(load_spinner,"spinner","")
			self.kernel_box_stack.add_titled(self.kernel_list_box,"kernels","")

			self.kernel_vp.add(self.kernel_box_stack)

			self.kernel_filter=''

			self.flag_installed=False
			self.kernel_combobox_spinner_active=False

			self.kernel_installed_filter_active=False
			self.switch_kernel_installed.set_state(False)
			self.switch_kernel_installed.set_sensitive(False)

			self.init_kernel_boot_store()
			self.connect_signals()
			self.set_css_info()
			self.load_kernels()


			
		except Exception as e:
			self.core.dprint("(KernelBox)Error: %s"%e,"[KernelBox]")
		
	#def __init__
	








	def set_css_info(self):

		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("first-aid-kit.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		
		self.info_box_kernel.set_name("PKG_BOX")
		self.separator_kernel.set_name("SEPARATOR")
		
		self.kernel_list_box.set_name("PKG_BOX")

		self.kernel_label.set_name("SECTION_LABEL")

		self.txt_check_kernel.set_name("INFO_LABEL")

		self.update_kernels_button.set_name("EXECUTE_BUTTON")
		self.filter_kernels_button.set_name("EXECUTE_BUTTON")
		self.apply_kernel_button.set_name("EXECUTE_BUTTON")
			
	#def set-css_info








	def connect_signals(self):

		
		self.update_kernels_button.connect("clicked",self.update_kernels_button_clicked)
		self.apply_kernel_button.connect("clicked",self.set_kernel_default)
		self.filter_kernels_button.connect("clicked",self.filter_kernels_button_clicked)
		self.entry_kernel.connect("activate",self.entries_press_event)
		self.switch_kernel_installed.connect("notify::active",self.kernel_installed_filter)
		
	#def connect_signals



	def entries_press_event(self,widget):
		
		self.filter_kernels_button_clicked(None)
		
	#def entries_press_event






	def init_kernel_boot_store(self):

		#PRINT KERNEL COMBOBOX

		#self.core.dprint("Combobox Kernel: %s"%self.kernel_installed_boot)
		renderer=Gtk.CellRendererText()
		self.kernel_combobox.pack_start(renderer,True)
		self.kernel_combobox.add_attribute(renderer,"text",0)
		self.kernel_installed_boot=Gtk.ListStore(str)
		self.kernel_combobox.set_model(self.kernel_installed_boot)
		self.kernel_combobox.set_active(0)

	#def kernel_boot



	def read_kernel_default(self):
		# SET IN COMBOBOX WICH KERNEL IS ACTIVE AT THE MOMENT.
		try:
			#print("######################READ KERNEL DEFAULT")
			#GRUB DEFAULT EXISTS? DEFINE POSITION, BUT NOT WICH KERNEL NUMBER
			grub_file='/etc/default/grub'
			f_orig=open(grub_file)
			lines=f_orig.readlines()
			f_orig.close()
			line_writed=False

			for line in lines:
				if "GRUB_DEFAULT=" in line:
					kernel_default_pos=line.replace('GRUB_DEFAULT=','')
					kernel_default_pos=kernel_default_pos.split()[0]
					#WE NEED DELETE ""
					kernel_default_pos=kernel_default_pos.replace('"','')
					token=">"
                    if token in kernel_default_pos:
					    break
					else:
                        kernel_default_pos="1>0"
				else:
					kernel_default_pos="1>0"


			######### ESTO FUNCIONA DE LUJO NO TOCAR ACUERDATE QUE POSEES COSAS ANULADAS ABAJO Y QUE LA GUI DE GLADE NO ESTA ORGANIZANDOME EL BOX COMO QUIERO
			#CHECK WICH KERNEL NUMBER IS ACTIVE, IF POSITION IS DEFINED IN GRUB DEFAUTL OR 0>0 BY DEFAULT.
			kernel_file="/tmp/.first-aid-kit_set-kernel.%s"%self.core.current_user
			os.system('/usr/share/first-aid-kit/grub-listmenu.sh > %s'%kernel_file)
			f=open(kernel_file)
			lines=f.readlines()
			f.close()
			os.remove(kernel_file)

			finded=False
			for line in lines:
				if kernel_default_pos in line:
					line=line.replace(kernel_default_pos,'')
					if "-generic" in line:
						line=line.replace('-generic','')
					if "LliureX 19" in line:
						line=line.replace('LliureX 19','')
					newstr = ''.join((ch if ch in '0123456789.-' else ' ') for ch in line)
					kernel_active = [str(i) for i in newstr.split()]
					finded=True
					break


			#SELECT KERNEL ACTIVE IN COMBOBOX
			pos=0
			if finded:
				for k in kernel_active:
					for i in self.kernel_installed_boot:
						element=(i[:])[0]
						#print ('%s element: %s'%(pos,element))
						if str(k)==str(element):
							#print 'eureka'
							#print pos
							return pos
						pos+=1

			return pos


		except Exception as e:
			return 0
			self.core.dprint("(read_kernel_default) Error: %s"%e,"[KernelBox]")
	#def read_kernel_default




	def set_kernel_default(self,widget):
		#SET KERNEL DEFAULT IN COMBOBOX
		try:
			it=self.kernel_combobox.get_active_iter()
			self.kernel_selected=self.kernel_installed_boot.get(it,0)[0]
			#self.kernel_po=self.eth_wharehouse[eth_selected]
			self.core.dprint("(set_kernel_default)Kernel default selected: %s  "%(self.kernel_selected),"[KernelBox]")

			kernel_file="/tmp/.first-aid-kit_set-kernel.%s"%self.core.current_user
			os.system('/usr/share/first-aid-kit/grub-listmenu.sh > %s'%kernel_file)
			f=open(kernel_file)
			lines=f.readlines()
			f.close()
			os.remove(kernel_file)

			
			for line in lines:
				if self.kernel_selected in line:
					if not "recovery" in line:
						default_grub_option=line.split()[0]

			self.core.dprint("(set_kernel_default)Kernel default position in Grub: %s"%(default_grub_option),"[KernelBox]")

			grub_file='/etc/default/grub'
			f_orig=open(grub_file)
			lines=f_orig.readlines()
			f_orig.close()

			grub_file_tmp='/tmp/.grub'
			f_copy=open(grub_file_tmp,"wt")

			line_writed=False
			for line in lines:
				if "GRUB_DEFAULT=" in line:
					f_copy.write('GRUB_DEFAULT="%s"'%default_grub_option)
					f_copy.write("\n")
					line_writed=True
				else:
					f_copy.write(line)
			
			if not line_writed:
				f_copy.write("GRUB_DEFAULT=%s\n"%default_grub_option)
			f_copy.close()

			shutil.copy(grub_file_tmp,grub_file)

			self.info_box_stack.set_visible_child_name("empty_box_kernel")
			self.switch_kernel_installed.set_sensitive(False)
			self.update_kernels_button.set_sensitive(False)
			self.filter_kernels_button.set_sensitive(False)
			self.apply_kernel_button.set_sensitive(False)
			self.entry_kernel.set_can_focus(False)
			self.kernel_box_stack.set_visible_child_name("spinner")

			allocation=self.kernel_combobox.get_allocation()
			w=allocation.width
			h=allocation.height

			self.kernel_combobox.hide()
			self.kernel_combobox_spinner.start()
			self.kernel_combobox_spinner.set_size_request(w,h)
			self.kernel_combobox_spinner.show()
			self.kernel_combobox_spinner_active=True

			self.thread_install=threading.Thread(target=self.set_kernel_default_thread)
			self.thread_install.daemon=True
			self.thread_install.start()

			GLib.timeout_add(500,self.check_set_kernel_default_thread)

		except Exception as e:
			self.core.dprint("(set_kernel_default) Error: %s"%e,"[KernelBox]")
	
	#def set_kernel_default



	def set_kernel_default_thread(self):

		try:
			self.core.working=True
			proc=subprocess.Popen('update-grub2',shell=True, stdin=None, stdout=open("/dev/null","w"), stderr=None, executable="/bin/bash")
			proc.wait()
		except Exception as e:
			self.core.dprint("(kernel_install_thread) Error: %s"%e,"[KernelBox]")	

	#def kernel_install_thread



	def check_set_kernel_default_thread(self):
		
		try:
			if self.thread_install.is_alive():
				return True
				
			self.flag_installed=True
			self.core.working=False

			self.kernel_box_stack.set_visible_child_name("kernels")
			self.update_kernels_button.set_sensitive(True)
			self.filter_kernels_button.set_sensitive(True)
			self.apply_kernel_button.set_sensitive(True)
			self.entry_kernel.set_can_focus(True)

			self.kernel_installed_spinner.hide()
			

			self.switch_kernel_installed.show()
			self.switch_kernel_installed.set_sensitive(True)
			
			self.kernel_combobox.set_active(self.read_kernel_default())
			self.kernel_combobox.show()
			self.kernel_combobox_spinner.hide()
			self.kernel_combobox_spinner_active=False

			self.info_box_stack.set_visible_child_name("info_kernel")
			a=_("You have a new kernel boot by defect:")
			self.txt_check_kernel.set_name("INFO_LABEL")
			self.txt_check_kernel.set_text("%s %s"%(a,self.kernel_selected))
			self.core.dprint("You have a new kernel boot by defect: %s"%self.kernel_selected,"[KernelBox]")

		except Exception as e:
			self.core.dprint("(check_set_kernel_default_thread) Error: %s"%e,"[KernelBox]")

	#def check_kernel_install_thread







	def kernel_installed_filter(self,widget,params):
		
		try:
			if self.switch_kernel_installed.get_active():
				self.kernel_installed_filter_active=True
			else:
				self.kernel_installed_filter_active=False

			self.switch_kernel_installed.set_sensitive(False)
			self.update_kernels_button.set_sensitive(False)
			self.filter_kernels_button.set_sensitive(False)
			self.apply_kernel_button.set_sensitive(False)
			self.entry_kernel.set_can_focus(False)
			self.kernel_box_stack.set_visible_child_name("spinner")


			allocation=self.switch_kernel_installed.get_allocation()
			w=allocation.width
			h=allocation.height
			
			self.switch_kernel_installed.hide()
			self.kernel_installed_spinner.start()
			self.kernel_installed_spinner.set_size_request(w,h)
			self.kernel_installed_spinner.show()

			self.info_box_stack.set_visible_child_name("info_kernel")
			self.txt_check_kernel.set_name("INFO_LABEL")
			self.txt_check_kernel.set_text(_("Applying filter to show only installed kernels...please wait"))
			self.core.dprint("Applying filter to show only installed kernels...please wait","[KernelBox]")

			self.show_kernel_results()

		except Exception as e:
			self.core.dprint("(kernel_installed_filter) Error: %s"%e,"[KernelBox]")
		
	#def kernel_installed_filter








	def filter_kernels_button_clicked (self,widget):
		try:
			self.entry_kernel.set_can_focus(False)
			self.kernel_filter=self.entry_kernel.get_text().split()
			#print self.kernel_filter
			self.update_kernels_button.set_sensitive(False)
			self.filter_kernels_button.set_sensitive(False)
			self.apply_kernel_button.set_sensitive(False)
			self.switch_kernel_installed.set_sensitive(False)
			self.kernel_box_stack.set_visible_child_name("spinner")

			self.info_box_stack.set_visible_child_name("info_kernel")
			self.txt_check_kernel.set_name("INFO_LABEL")
			self.txt_check_kernel.set_text(_("Applying filter to kernels...please wait"))
			self.core.dprint("Applying filter to kernels...","[KernelBox]")
			self.load_kernels()
			

		except Exception as e:
			self.core.dprint("(filter_kernels_button_clicked) Error: %s"%e,"[KernelBox]")

	#def filter_kernels_button_clicked







	def update_kernels_button_clicked (self,widget):
		try:

			self.entry_kernel.set_can_focus(False)
			self.kernel_filter=self.entry_kernel.get_text().split()
			self.update_kernels_button.set_sensitive(False)
			self.filter_kernels_button.set_sensitive(False)
			self.apply_kernel_button.set_sensitive(False)
			self.switch_kernel_installed.set_sensitive(False)
			
			for i in self.kernel_list_box:
				self.kernel_list_box.remove(i)

			self.kernel_box_stack.set_visible_child_name("spinner")
			self.kernel_box_stack.set_size_request(0,0)

			allocation=self.kernel_combobox.get_allocation()
			w=allocation.width
			h=allocation.height
			
			self.kernel_combobox.hide()
			self.kernel_combobox_spinner.start()
			self.kernel_combobox_spinner.set_size_request(w,h)
			self.kernel_combobox_spinner.show()
			self.kernel_combobox_spinner_active=True

			self.info_box_stack.set_visible_child_name("info_kernel")
			self.txt_check_kernel.set_name("INFO_LABEL")
			self.txt_check_kernel.set_text(_("Updating Kernel Cache...please wait"))
			self.core.dprint("Updating Kernel Cache...","[KernelBox]")
			
			self.thread_up=threading.Thread(target=self.update_kernels_thread)
			self.thread_up.daemon=True
			self.thread_up.start()

			self.kernel_vp.set_size_request(0,0)
			self.kernel_sw.get_vadjustment().set_page_size(0)
			self.kernel_sw.get_hadjustment().set_page_size(0)
			self.kernel_sw.set_size_request(0,0)


			GLib.timeout_add(500,self.check_update_kernels_thread)

		except Exception as e:
			self.core.dprint("(update_kernels_button_clicked) Error: %s"%e,"[KernelBox]")

	#def update_kernels_button_clicked



	def update_kernels_thread(self):

		try:

			self.cache.update()
				
		except Exception as e:
			self.core.dprint("(update_kernels_thread) Error: %s"%e,"[KernelBox]")	

	#def update_kernels_thread



	def check_update_kernels_thread(self):
		
		try:
			if self.thread_up.is_alive():
				return True

			self.load_kernels()

		except Exception as e:
			self.core.dprint("(check_update_kernels_thread) Error: %s"%e,"[KernelBox]")

	#def check_update_kernels_thread








	def load_kernels(self):

		try:
			self.entry_kernel.set_can_focus(False)
			self.update_kernels_button.set_sensitive(False)
			self.filter_kernels_button.set_sensitive(False)
			self.apply_kernel_button.set_sensitive(False)
			self.switch_kernel_installed.set_sensitive(False)
			self.switch_kernel_installed.set_sensitive(False)


			
			self.read_kernels()
				
		except Exception as e:
			self.core.dprint("(load_kernels) Error: %s"%e,"[KernelBox]")	

	#def load_kernels




	def read_kernels(self):

		try:
			if self.kernel_combobox_spinner_active:

				allocation=self.kernel_combobox.get_allocation()
				w=allocation.width
				h=allocation.height
				
				self.kernel_combobox.hide()
				self.kernel_combobox_spinner.start()
				self.kernel_combobox_spinner.set_size_request(w,h)
				self.kernel_combobox_spinner.show()

			self.thread=threading.Thread(target=self.read_kernels_thread)
			self.thread.daemon=True
			self.thread.start()

			self.core.dprint("Reading kernels avaiables..........","[KernelBox]")
			self.kernel_installed_boot.clear()
			GLib.timeout_add(500,self.check_read_kernels_thread)

		except Exception as e:
			self.core.dprint("(read_kernels) Error: %s"%e,"[KernelBox]")

	#def read_kernels



	def read_kernels_thread(self):
		try:

			platform.architecture()[0]
			if '64' in platform.architecture()[0]:
				self.arch64=True
			else:
				self.arch64=False

			self.cache=apt.cache.Cache()

			pkgs=[pkg for pkg in self.cache]

			self.avaiable=[]
			self.installed=[]
			self.kernel_count_orig=0
			
			for i in pkgs:
				if not 'linux-headers-generic' == str(i):
					if 'linux-header' in str(i):
						if 'generic' in str(i):
							version=str(i)
							linux_image=version.replace('linux-headers-','linux-image-')
							version=version.replace('linux-headers-','')
							version=version.replace('generic-','')
							version=version.replace('-generic','')
							if self.arch64:
								if  not 'i386' in str(i):
									if self.cache[str(i)].is_installed:
										self.installed.append(version)
										self.avaiable.append((version,str(i),True,linux_image))

										self.kernel_installed_boot.append([version])
										self.kernel_count_orig=self.kernel_count_orig+1
										#print ('%s is installed'%version)
									else:
										
										self.avaiable.append((version,str(i),False,linux_image))
										#print i
							else:
								if 'i386' in str(i):
									if self.cache[str(i)].is_installed:
										self.installed.append(version)
										self.avaiable.append((version,str(i),True,linux_image))
										self.kernel_installed_boot.append([version])
										self.kernel_count_orig=self.kernel_count_orig+1
										#print ('%s is installed'%version)
									else:
										self.avaiable.append((version,str(i),False,linux_image))

			#self.kernel_boot()
			self.filtered=[]
			if len(self.kernel_filter)>0:
				#print 'In filter....'
				for i in self.avaiable:
					add=True
					#print i
					for option in self.kernel_filter:
						#print 'Apply filter:   %s'%option
						if not str(option) in str(i[1]):
							add=False
					if add:
						#print "** Added **"
						self.filtered.append(i)

				self.avaiable=self.filtered



			#print self.avaiable

		except Exception as e:
			self.core.dprint("(read_kernels_thread) Error: %s"%e,"[KernelBox]")

	#def read_kernels


	def check_read_kernels_thread(self):
		
		try:
			if self.thread.is_alive():
				return True

			self.show_kernel_results()

		except Exception as e:
			self.core.dprint("(check_read_kernels_thread) Error: %s"%e,"[KernelBox]")

	#def check_read_kernels_thread




	def show_kernel_results(self):
		try:

			#count=len(self.avaiable)
			count=0

			for i in self.kernel_list_box:
				self.kernel_list_box.remove(i)

			#self.core.lprint("*****Kernels avaiables*****","[KernelBox]")
			for kernel in self.avaiable:
				#self.core.lprint(str(kernel),"[KernelBox]")

				if self.kernel_installed_filter_active:
					if kernel[2]:
						count=count+1
						self.generate_element_list(kernel)
				else:
					count=count+1
					self.generate_element_list(kernel)
				
				count-=1
				if count>0:
					s=Gtk.Separator()
					s.show()
					self.kernel_list_box.pack_start(s,False,False,5)
					self.kernel_list_box.set_margin_bottom(20)
					self.kernel_list_box.set_margin_top(5)
					self.kernel_list_box.set_margin_left(9)
					self.kernel_list_box.set_margin_right(9)

			self.kernel_box_stack.set_visible_child_name("kernels")
			self.update_kernels_button.set_sensitive(True)
			self.filter_kernels_button.set_sensitive(True)
			self.apply_kernel_button.set_sensitive(True)
			self.entry_kernel.set_can_focus(True)

			self.kernel_installed_spinner.hide()
			

			self.switch_kernel_installed.show()
			self.switch_kernel_installed.set_sensitive(True)
			
			self.kernel_combobox.set_active(self.read_kernel_default())
			self.kernel_combobox.show()
			self.kernel_combobox_spinner.hide()
			self.kernel_combobox_spinner_active=False
			
			if not self.flag_installed:
				self.info_box_stack.set_visible_child_name("empty_box_kernel")
			else:
				self.info_box_stack.set_visible_child_name("info_kernel")
				a=_("Your new kernel list:")
				self.txt_check_kernel.set_name("INFO_LABEL")
				self.txt_check_kernel.set_text("%s\n%s"%(a,self.installed))
				self.flag_installed=False

		except Exception as e:
			self.core.dprint("(show_kernel_results) Error: %s"%e,"[KernelBox]")
	
	#def show_kernel_results






	def generate_element_list(self,kernel):
		try:
			hbox=Gtk.HBox()
			label=Gtk.Label(kernel[0])
			label.set_alignment(0,0)
			#cb=Gtk.CheckButton()
			cb=Gtk.Button()
			cb.set_halign(Gtk.Align.END)
			hbox.pack_start(label,True,True,0)
			hbox.pack_end(cb,True,True,0)
			hbox.set_margin_left(10)
			hbox.set_margin_right(10)
			hbox.show_all()

			cb.label=label.get_text()
			cb.data=kernel
			hbox.checkbutton=cb
			if kernel[2]:
				#hbox.checkbutton.set_active(True)
				hbox.checkbutton.set_label(_("Uninstall"))
				hbox.checkbutton.set_name("UNINSTALL_BUTTON")
				hbox.checkbutton.connect("clicked",self.uninstall_clicked)
			else:
				hbox.checkbutton.set_label(_("Install"))
				hbox.checkbutton.set_name("INSTALL_BUTTON")
				hbox.checkbutton.connect("clicked",self.install_clicked)
			
			#hbox.set_name("PKG_BOX")

			tmp=Gtk.EventBox()
			tmp.add(hbox)
			tmp.show_all()
			tmp.add_events( Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK )
			tmp.connect("motion-notify-event",self.mouse_over_kernel)
			tmp.connect("leave_notify_event",self.mouse_left_kernel)
			self.kernel_list_box.pack_start(tmp,False,False,5)

		except Exception as e:
			self.core.dprint("(generate_element_list) Error: %s"%e,"[KernelBox]")
	
	#def generate_element_list

	def mouse_over_kernel(self,eb,event):

		eb.set_name("KERNEL_OVER")

	#def mouse_over_kernel


	def mouse_left_kernel(self,eb,event):

		eb.set_name("KERNEL_REGULAR")

	#def mouse_over_kernel


	def uninstall_clicked(self,widget):

		try:
			#CANCEL OPERATION IF THIS KERNEL IS IN USE AT THE MOMENT OR KERNEL IS IN META LLIUREX
			kernel_file='/tmp/.uname'
			os.system('uname -r > %s'%kernel_file)
			f=open(kernel_file)
			lines=f.readlines()
			f.close()
			os.remove(kernel_file)

			for line in lines:
				if widget.label in line:
					mw=self.core.lri.main_window
					d=Dialog.InfoDialog(mw,_("First Aid Kit"),_("You can't delete this kernel because you are using now."))
					response=d.run()
					d.destroy()
					self.core.dprint("You can't delete this kernel because you are using now: %s"%(widget.label),"[KernelBox]")
					self.update_kernels_button.set_sensitive(True)
					self.filter_kernels_button.set_sensitive(True)
					self.apply_kernel_button.set_sensitive(True)
					self.entry_kernel.set_can_focus(True)
					self.switch_kernel_installed.set_sensitive(True)

					return True

			# CANCEL OPERATION IF LLIUREX-META I AFFECTED WITH THIS OPERATION
			kernel_file='/tmp/.uname'
			os.system('LANG=C apt show linux-headers-generic > %s'%kernel_file)
			f=open(kernel_file)
			lines=f.readlines()
			f.close()
			os.remove(kernel_file)

			for line in lines:
				if 'Depends' in line:
					if widget.label in line:
						mw=self.core.lri.main_window
						a=_("First Aid Kit")
						b=_("You can't delete this kernel because is essential for LliureX.")
						d=Dialog.InfoDialog(mw,a,b)
						response=d.run()
						d.destroy()
						self.core.dprint("You can't delete this kernel because is essential for LliureX: %s"%(widget.label),"[KernelBox]")
						self.update_kernels_button.set_sensitive(True)
						self.filter_kernels_button.set_sensitive(True)
						self.apply_kernel_button.set_sensitive(True)
						self.entry_kernel.set_can_focus(True)
						self.switch_kernel_installed.set_sensitive(True)

						return True



			mw=self.core.lri.main_window
			a = _("First Aid Kit")
			b = _("Do you want to DELETE this kernel?")
			d=Dialog.QuestionDialog(mw,a,("%s\n%s"%(b,widget.label)))


			response=d.run()
			d.destroy()
			if response== Gtk.ResponseType.OK:
				self.info_box_stack.set_visible_child_name("info_kernel")
				self.core.dprint('delete    %s      %s'%(widget.label,[widget.data[1],widget.data[3]]),"[KernelBox]")
				self.kernel_install('delete',widget.label,[widget.data[1],widget.data[3]])				
			else:
				self.info_box_stack.set_visible_child_name("info_kernel")
				a = _("You cancel to uninstall kernel:")
				self.txt_check_kernel.set_name("INFO_LABEL")
				self.txt_check_kernel.set_text(_("%s %s")%(a,widget.label))
				self.core.dprint("You cancel to uninstall kernel: %s"%(widget.label),"[KernelBox]")
				self.update_kernels_button.set_sensitive(True)
				self.filter_kernels_button.set_sensitive(True)
				self.apply_kernel_button.set_sensitive(True)
				self.entry_kernel.set_can_focus(True)
				self.switch_kernel_installed.set_sensitive(True)

		except Exception as e:
			self.core.dprint("(uninstall_clicked) Error: %s"%e,"[KernelBox]")
			self.info_box_stack.set_visible_child_name("info_kernel")
			a=_("(uninstall_clicked) Error:")
			self.txt_check_kernel.set_name("INFO_LABEL_ERROR")
			self.txt_check_kernel.set_text("%s %s"%(a,e))

	#def uninstall_clicked




	def install_clicked(self,widget):

		try:
			mw=self.core.lri.main_window
			a=_("Do you want to INSTALL this kernel?")
			d=Dialog.QuestionDialog(mw,_("First Aid Kit"),_("%s\n%s"%(a,widget.label)))
			response=d.run()
			d.destroy()
			if response== Gtk.ResponseType.OK:
				self.info_box_stack.set_visible_child_name("info_kernel")
				self.core.dprint('install    %s      %s'%(widget.label,[widget.data[1],widget.data[3]]),"[KernelBox]")
				self.kernel_install('install',widget.label,[widget.data[1],widget.data[3]])			
			else:
				self.info_box_stack.set_visible_child_name("info_kernel")
				a=_("You cancel to install kernel:")
				self.txt_check_kernel.set_name("INFO_LABEL")
				self.txt_check_kernel.set_text(_("%s %s")%(a,widget.label))
				self.core.dprint("%s %s"%(a,widget.label),"[KernelBox]")
				self.update_kernels_button.set_sensitive(True)
				self.filter_kernels_button.set_sensitive(True)
				self.apply_kernel_button.set_sensitive(True)
				self.entry_kernel.set_can_focus(True)
				self.switch_kernel_installed.set_sensitive(True)

		except Exception as e:
			self.core.dprint("(install_clicked) Error: %s"%e,"[KernelBox]")
			self.info_box_stack.set_visible_child_name("info_kernel")
			self.txt_check_kernel.set_name("INFO_LABEL_ERROR")
			self.txt_check_kernel.set_text(_("(install_clicked) Error: %s"%e))

	#def install_clicked




	def kernel_install(self,action,kernel_label,packages):

		try:

			for i in self.kernel_list_box:
				self.kernel_list_box.remove(i)

			self.kernel_box_stack.set_visible_child_name("spinner")

			self.entry_kernel.set_can_focus(False)
			self.update_kernels_button.set_sensitive(False)
			self.filter_kernels_button.set_sensitive(False)
			self.apply_kernel_button.set_sensitive(False)
			self.switch_kernel_installed.set_sensitive(False)

			allocation=self.kernel_combobox.get_allocation()
			w=allocation.width
			h=allocation.height
			
			self.kernel_combobox.hide()
			self.kernel_combobox_spinner.start()
			self.kernel_combobox_spinner.set_size_request(w,h)
			self.kernel_combobox_spinner.show()
			self.kernel_combobox_spinner_active=True

			if action == 'install':
				for app in packages:
					#Install linux-headers and linux-generic packages
					pkg=self.cache[app]
					pkg.mark_install()
					label_action=_('Installing')

			if action == 'delete':
				for app in packages:
					#Delete linux-headers and linux-generic packages
					pkg=self.cache[app]
					pkg.mark_delete()
					label_action=_('Deleting')

			self.info_box_stack.set_visible_child_name("info_kernel")
			a=_("Please wait.....")
			self.txt_check_kernel.set_name("INFO_LABEL")
			self.txt_check_kernel.set_text(_("%s: %s  %s"%(label_action,kernel_label,a)))
			#self.core.dprint("%s: %s  %s"%(label_action,kernel_label,a),"KernelBox")
			self.core.dprint("Action: %s  Kernel: %s  Packages: %s"%(action,kernel_label,str(packages)),"[KernelBox]")
			
			self.thread_install=threading.Thread(target=self.kernel_install_thread)
			self.thread_install.daemon=True
			self.thread_install.start()

			GLib.timeout_add(500,self.check_kernel_install_thread)

		except Exception as e:
			self.core.dprint("(kernel_install) Error: %s"%e,"[KernelBox]")

	#def install_clicked


	def kernel_install_thread(self):

		try:
			self.core.working=True
			self.core.dprint("(kernel_install_thread) (cache.commit) Start........","[KernelBox]")
			commit=self.cache.commit()
			self.core.dprint("Commit result is: %s"%commit,"[KernelBox]")
			self.core.dprint("(kernel_install_thread) (cache.commit) Finished........","[KernelBox]")

			proc=subprocess.Popen('update-grub2',shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")

			for line in iter(proc.stderr.readline,""):
				line=line.strip("\n")
				self.core.dprint("(kernel_install_thread) Subprocess stdout: %s"%line,"[KernelBox]")
				
				#self.core.lprint("(kernel_install_thread) Subprocess stderr: %s"%stderr,"[KernelBox]")
			proc.wait()
		except Exception as e:
			self.core.dprint("(kernel_install_thread) Error: %s"%e,"[KernelBox]")	

	#def kernel_install_thread



	def check_kernel_install_thread(self):
		
		try:
			if self.thread_install.is_alive():
				return True
				
			self.flag_installed=True
			self.load_kernels()
			self.core.working=False
			self.core.dprint("Finished!!","[KernelBox]")

		except Exception as e:
			self.core.dprint("(check_kernel_install_thread) Error: %s"%e,"[KernelBox]")

	#def check_kernel_install_thread

