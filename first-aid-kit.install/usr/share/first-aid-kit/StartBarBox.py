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

import pexpect
import re
import hashlib
import binascii
import getpass
import sys
import secrets

gettext.textdomain('first-aid-kit')
_=gettext.gettext


RSRC="./rsrc/"


class StartBarBox(Gtk.VBox):
	
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain('first-aid-kit')
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

		self.start_bar_box32=builder.get_object("box32")
		self.grub_passwd_button=builder.get_object("grub_passwd_button")
		self.grub_passwd_button_box=builder.get_object("grub_passwd_button_box")
		self.grub_passwd_spinner=builder.get_object("grub_passwd_spinner")
		self.grub_passwd_label=builder.get_object("grub_passwd_label")

		self.grub_passwd_window=builder.get_object("grub_passwd_window")
		self.user_grub_label=builder.get_object("user_grub_label")
		self.accept_grub_button=builder.get_object("accept_grub_button")
		self.cancel_grub_button=builder.get_object("cancel_grub_button")
		self.grub_user_title=builder.get_object("grub_user_title")
		self.passwd_grub_label=builder.get_object("passwd_grub_label")
		self.grub_passwd_title=builder.get_object("grub_passwd_title")

		self.grub_user_title.set_text(_("Insert user for GRUB:"))
		self.grub_passwd_title.set_text(_("Insert password for GRUB:"))
		

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

		#test if passwd is configured in GRUB
		self.grub_default_file='/etc/default/grub'
		self.grub_custom_file="/etc/grub.d/40_custom"
		self.grub_linux_file="/etc/grub.d/10_linux"
		self.grub_default_word = 'GRUB_DISABLE_SUBMENU=y'
		self.grub_custom_word='set superusers='
		self.grub_custom_word2='password_pbkdf2 '
		self.grub_passwd=' grub.pbkdf2.sha512.10000.1B5DE39EC649A0372C6D27A7C60B54199CD094BBA2CB53DB0AFCC64AE699F7C2EDF6304B43D4919F846209E808C600C381C34A40F65F636FD196AB55C54D6DC2.65A2E205C9F4E1A1FAE1040E5655C2CD94B3ED5CC8010D5DE80DD70F747D14A98CE5F4554D88A299A26E173F79594B41206055B69F9E1E66602DE94F84E60CB2'
		self.grub_passwd2=self.grub_passwd
		f = open(self.grub_default_file,'r')
		for line in f:
			if self.grub_default_word in line:
				self.grub_passwd_active=True
				self.grub_passwd_button.set_label(_("Deactivate"))
				break
			else:
				self.grub_passwd_active=False
				self.grub_passwd_button.set_label(_("Activate"))
		f.close()



		self.grub_file='/etc/default/grub.d/06-lliurex-cmdline.cfg'
		self.word = 'splash '
		try:
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
		except Exception as e:
			self.splash_delete=False
			self.start_bar_button.set_label(_("Delete Startup Bar"))
			self.info_box_stack.set_visible_child_name("empty_box_start_bar")
	
	#def __init__
	




	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path("first-aid-kit.css")
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		
		self.start_bar_button.set_name("EXECUTE_BUTTON")
		self.grub_passwd_button.set_name("EXECUTE_BUTTON")
		self.start_bar_box2.set_name("PKG_BOX")
		self.start_bar_box32.set_name("PKG_BOX")
		self.info_box.set_name("PKG_BOX")
		self.separator1.set_name("SEPARATOR_MAIN")

		self.section_label_4.set_name("SECTION_LABEL")
		self.label1.set_name("OPTION_LABEL")
		self.grub_passwd_label.set_name("OPTION_LABEL")
		self.txt_check_start_bar.set_name("INFO_LABEL")
		self.grub_user_title.set_name("OPTION_LABEL")
		self.grub_passwd_title.set_name("OPTION_LABEL")
			
	#def set-css_info



	def connect_signals(self):
		
		self.start_bar_button.connect("clicked",self.start_bar_button_clicked)
		self.grub_passwd_button.connect("clicked",self.grub_passwd_button_clicked)

		self.accept_grub_button.connect("clicked",self.accept_grub_button_clicked)
		self.cancel_grub_button.connect("clicked",self.cancel_grub_button_clicked)
		self.user_grub_label.connect("activate",self.entries_press_event)

		self.grub_passwd_window.connect("delete_event",self.hide_window)
		
	#def connect_signals


	def entries_press_event(self,widget):
		
		self.accept_grub_button_clicked(None)
		
	#def entries_press_event


	def hide_window(self,widget,event):
		
		widget.hide()
		self.grub_passwd_spinner.hide()
		self.grub_passwd_button.show()
		self.grub_passwd_button.set_sensitive(True)
		self.start_bar_button.set_sensitive(True)
		self.username_empty=True
		return True
		
	#def hide_window




	def start_bar_button_clicked(self,widget):

		self.start_bar_button.set_sensitive(False)
		self.grub_passwd_button.set_sensitive(False)		
		self.thread=threading.Thread(target=self.start_bar_button_thread)
		self.thread.daemon=True
		self.thread.start()
		
		allocation=self.start_bar_button.get_allocation()
		w=allocation.width
		h=allocation.height

		self.start_bar_button.hide()
		self.start_bar_spinner.start()
		self.start_bar_spinner.set_size_request(w,h)
		self.start_bar_spinner.show()
		self.txt_check_start_bar.set_name("INFO_LABEL")

		GLib.timeout_add(500,self.check_start_bar_thread)
	
	#start_bar_button_clicked



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
		self.grub_passwd_button.set_sensitive(True)
		self.start_bar_button.set_sensitive(True)
		self.info_box_stack.set_visible_child_name("empty_box_start_bar")
		
	#check_gparted_thread


















	def cancel_grub_button_clicked(self,widget):
		
		self.grub_passwd_window.hide()
		self.grub_passwd_spinner.hide()
		self.grub_passwd_button.show()
		self.grub_passwd_button.set_sensitive(True)
		self.start_bar_button.set_sensitive(True)
		self.username_empty=True
		
	#def cancel_grub_button



	def accept_grub_button_clicked(self,widget):
		
		self.grub_passwd_window.hide()
		self.info_box_stack.set_visible_child_name("empty_box_start_bar")
		self.user_grub_label.set_can_focus(False)
		self.user_grub=self.user_grub_label.get_text().split()
		self.passwd_grub=self.passwd_grub_label.get_text().split()
		self.core.dprint(self.user_grub,"[StarBarBox] user:")
		self.core.dprint(self.passwd_grub,"[StarBarBox] passwd:")

		if len(self.user_grub)==1 and len(self.passwd_grub)==1:

			self.user_grub=self.user_grub[0]
			self.passwd_grub=self.passwd_grub[0]

			if self.user_grub=='' or self.passwd_grub=='':
				self.grub_passwd_spinner.hide()
				self.grub_passwd_button.show()
				self.grub_passwd_button.set_sensitive(True)
				self.start_bar_button.set_sensitive(True)
				self.txt_check_start_bar.set_name("INFO_LABEL_ERROR")
				self.txt_check_start_bar.set_text(_("Username or Password is empty, the process is canceled."))
				self.info_box_stack.set_visible_child_name("info_start_bar")
			else:
				self.grub_passwd_button_launched(widget)
			

		else:

			self.grub_passwd_spinner.hide()
			self.grub_passwd_button.show()
			self.grub_passwd_button.set_sensitive(True)
			self.start_bar_button.set_sensitive(True)
			self.txt_check_start_bar.set_name("INFO_LABEL_ERROR")
			self.txt_check_start_bar.set_text(_("Username can't contain blank spaces."))
			self.info_box_stack.set_visible_child_name("info_start_bar")

		
	#def accept_grub_button



	def grub_passwd_button_clicked(self,widget):

		self.start_bar_button.set_sensitive(False)
		self.grub_passwd_button.set_sensitive(False)
		self.info_box_stack.set_visible_child_name("empty_box_start_bar")
		self.txt_check_start_bar.set_name("INFO_LABEL")
		self.txt_check_start_bar.set_text("")
		self.user_grub_label.set_text("")
		if self.grub_passwd_active == False:
			self.user_grub_label.set_can_focus(True)
			self.grub_passwd_window.show()
		else:
			self.grub_passwd_button_launched(widget)

	#grub_passwd_button_clicked




	def grub_passwd_button_launched(self,widget):
		
		self.thread=threading.Thread(target=self.grub_passwd_button_thread)
		self.thread.daemon=True
		self.thread.start()
		
		allocation=self.grub_passwd_button.get_allocation()
		w=allocation.width
		h=allocation.height

		self.grub_passwd_button.hide()
		self.grub_passwd_spinner.start()
		self.grub_passwd_spinner.set_size_request(w,h)
		self.grub_passwd_spinner.show()
		self.info_box_stack.set_visible_child_name("empty_box_start_bar")

		GLib.timeout_add(500,self.check_grub_passwd_thread)
	
	#grub_passwd_button_clicked


	def grub_passwd_button_thread(self):
	
		try:
			
			self.core.working=True
			
			if self.grub_passwd_active == True:
				#Operations in /etc/default/grub
				self.core.dprint("Passwd is activate in GRUB, now you're deactivating it....... please wait.","[StarBarBox]")
				f = open(self.grub_default_file,'r')
				lst = []
				for line in f:
					if self.grub_default_word in line:
						pass
					else:
						lst.append(line)
				f.close()
				f = open(self.grub_default_file,'w')
				for line in lst:
					f.write(line)
				f.close()

				#Operations in /etc/grub.d/40_custom
				d = open(self.grub_custom_file,'r')
				lstd = []
				for line in d:
					lstd.append(line)
				d.close()
				d = open(self.grub_custom_file,'w')
				for line in lstd:
					if self.grub_custom_word in line:
						pass
					else:
						if self.grub_custom_word2 in line:
							pass 
						else:
							d.write(line)
				d.close()



				#Operations in /etc/grub.d/10_linux
				fd = open(self.grub_linux_file,'r')
				lst = []
				match="grub_quote)' ${CLASS} --unrestricted"
				replace="grub_quote)' ${CLASS}"
				for line in fd:
					if match in line:
						line = line.replace(match,replace)
					lst.append(line)
				fd.close()
				fd = open(self.grub_linux_file,'w')
				for line in lst:
					fd.write(line)
				fd.close()


				self.grub_passwd_active = False
				self.grub_passwd_button.set_label(_("Activate"))
				self.info_box_stack.set_visible_child_name("info_start_bar")
				self.txt_check_start_bar.set_text(_("The GRUB passwd is removing from your system, applying changes....."))
				os_message="GRUB passwd is deactivated."
				
				
			else:
				#Operations in /etc/default/grub
				self.core.dprint("Passwd is deactivate in GRUB, now you're activating it....... please wait.","[StarBarBox]")
				'''proc = pexpect.spawn("grub-mkpasswd-pbkdf2", encoding="utf-8", timeout=15, env={**os.environ, "LC_ALL": "C"})
				
				#self.core.dprint("2.1 Proceso iniciado", "[StarBarBox]")
				proc.expect("Enter password:")
				#self.core.dprint("2.2 Solicitud de contraseña detectada", "[StarBarBox]")

				proc.sendline(str(self.passwd_grub))
				#self.core.dprint("2.3 Primera contraseña enviada", "[StarBarBox]")

				proc.expect("Reenter password:")
				#self.core.dprint("2.4 Solicitud de confirmación detectada", "[StarBarBox]")

				proc.sendline(str(self.passwd_grub))
				#self.core.dprint("2.5 Segunda contraseña enviada", "[StarBarBox]")

				proc.expect(pexpect.EOF)
				#self.core.dprint("3. Proceso finalizado", "[StarBarBox]")

				match = re.search(r"grub\.pbkdf2\.sha512\.[^\s]+", proc.before)
				self.grub_passwd = match.group(0) if match else None
				self.grub_passwd =self.grub_passwd.strip()'''
				
				self.grub_passwd=self.generar_hash_grub(self.passwd_grub)
				self.core.dprint(self.grub_passwd,"[StarBarBox] Passwd Hash:")
				self.validar_hash_grub(self.grub_passwd, self.passwd_grub)
				#self.grub_passwd=self.grub_passwd2
				with open(self.grub_default_file, 'a') as file:
					file.write(self.grub_default_word+'\n')

				#Operations in /etc/grub.d/40_custom
				with open(self.grub_custom_file, 'a') as file:
					file.write(self.grub_custom_word+'"'+self.user_grub+'"'+'\n')
					file.write(self.grub_custom_word2+self.user_grub+' '+self.grub_passwd+'\n')

				#Operations in /etc/grub.d/10_linux
				fd = open(self.grub_linux_file,'r')
				lst = []
				match="grub_quote)' ${CLASS}"
				replace="grub_quote)' ${CLASS} --unrestricted"
				for line in fd:
					if match in line:
						line = line.replace(match,replace)
					lst.append(line)
				fd.close()
				fd = open(self.grub_linux_file,'w')
				for line in lst:
					fd.write(line)
				fd.close()

				self.grub_passwd_active = True
				self.grub_passwd_button.set_label(_("Deactivate"))
				self.info_box_stack.set_visible_child_name("info_start_bar")
				self.txt_check_start_bar.set_text(_("The GRUB passwd is adding in your system, applying changes....."))
				os_message="GRUB passwd is activated."


			os.chmod(self.grub_custom_file, 0o700)
			os.system('update-grub')
			self.core.dprint(os_message,"[StarBarBox]")
			time.sleep(1)
			self.thread_ret={"status":True,"msg":"BROKEN"}
			
		except Exception as e:
			self.core.dprint("(start_bar_button_thread)Error: %s"%e,"[StarBarBox]")
			return False

	#grub_passwd_button_thread
			





	def check_grub_passwd_thread(self):
		
		if self.thread.is_alive():
			return True
		
		self.core.working=False
		self.info_box_stack.set_visible_child_name("empty_box_start_bar")
		self.grub_passwd_spinner.hide()
		self.grub_passwd_button.show()
		self.grub_passwd_button.set_sensitive(True)
		self.start_bar_button.set_sensitive(True)
		if self.grub_passwd_active:
			self.txt_check_start_bar.set_text(_("GRUB has activated passwd to %s user, the passwd is %s.")%(self.user_grub, self.passwd_grub))
		else:
			self.txt_check_start_bar.set_text(_("GRUB has not passwd, anyone can edit it."))
		self.info_box_stack.set_visible_child_name("info_start_bar")

		
	#check_grub_passwd_thread
	
	
	
	
	
	def validar_hash_grub(self, grub_hash,password):
		print("--- Verificador de contraseña para GRUB (PBKDF2) ---")

		# El hash generado por grub-mkpasswd-pbkdf2
		self.core.dprint(grub_hash,"[StarBarBox] Comprobando el Hash:")

		#La contraseña a validar
		self.core.dprint(password,"[StarBarBox] Contraseña a validar:")

		try:
			# El hash de GRUB tiene el formato: grub.pbkdf2.sha512.iteraciones.salt.hash
			parts = grub_hash.split(".")

			if len(parts) != 6 or parts[0] != "grub" or parts[1] != "pbkdf2" or parts[2] != "sha512":
				self.core.dprint("❌ Error: El formato del hash no parece un hash válido de GRUB (grub.pbkdf2.sha512...)","[StarBarBox]")
				return

			iterations = int(parts[3])
			salt = binascii.unhexlify(parts[4])
			original_key = binascii.unhexlify(parts[5])

			# Calcular el hash con la contraseña introducida para comparar
			calculated_key = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, iterations)

			if calculated_key == original_key:
				self.core.dprint("✅ ¡Validación correcta! La contraseña coincide perfectamente con el hash.","[StarBarBox]")
			else:
				self.core.dprint("❌ Error: La contraseña NO corresponde a ese hash.","[StarBarBox]")

		except Exception as e:
			self.core.dprint("(start_bar_button_thread)Error: %s"%e,"[StarBarBox]")
			
	#validar_hash_grub
	
	
	
	def generar_hash_grub(self,password):
		try:
			self.core.dprint("--- Generador de Hash para GRUB (PBKDF2) ---","[StarBarBox]")

			# Parámetros estándar que usa GRUB de forma nativa
			iteraciones = 10000
			longitud_salt = 64  # 64 bytes de sal aleatoria

			# Generar una sal aleatoria segura y convertirla a hexadecimal
			salt_bytes = secrets.token_bytes(longitud_salt)
			salt_hex = salt_bytes.hex().lower()

			# Calcular el hash PBKDF2 con SHA-512
			hash_bytes = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt_bytes, iteraciones)
			hash_hex = hash_bytes.hex().lower()

			# Construir la estructura final idéntica a grub-mkpasswd-pbkdf2
			grub_formatted_hash = f"grub.pbkdf2.sha512.{iteraciones}.{salt_hex}.{hash_hex}"
			
			self.core.dprint("✅ Hash generado con éxito:","[StarBarBox]")
			return grub_formatted_hash
		
		except Exception as e:
			self.core.dprint("(start_bar_button_thread)Error: %s"%e,"[StarBarBox]")
			
	#generar_hash_grub