import xmlrpclib

class N4dManager:
	
	
	
	def __init__(self):
		
		
		pass
		
	#def init

	
	def validate_user(self,username,password,server_ip):
		
		try:
			if server_ip in {'',None}:
				server_ip="server"
			if server_ip in {'localhost'}:
				proxy="https://localhost:9779"
				#print proxy
				self.client=xmlrpclib.ServerProxy(proxy)
			else:
				proxy="https://%s:9779"%server_ip
				#print proxy
				self.client=xmlrpclib.ServerProxy(proxy)
			
			self.server=server_ip
				
			ret=self.client.validate_user(username,password)
			if ret[0]:
				if "admins" in ret[1]:
					self.user=(username,password)
					return [True,""]
				else:
					return [False,"User is not allowed to use this application, only netadmins users"]
					
			return [False,"Wrong user and/or password"]
			
		except Exception as e:
			print e
			return [False,str(e)]
		
		
	#def validate_user
	
	
	
#class n4dmanager