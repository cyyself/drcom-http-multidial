#!/usr/bin/env python3
import os
from time import *
#CONFIG BEGIN
authserver = "202.202.0.163"
# 202.202.0.163 for CQU Campus A and B, 10.254.7.4 for CQU Campus D (Huxi)
# We deprecated IPv6 in this version, you can just add "curl -L -6 $SOME_V6_HTTP_URL" to crontab to keep ipv6 alive
conn = [
	{
		"username":"2018xxxx",
		"password":"233333", 	# If there is ' in your password, you should manually escape
		"R6":"0", 				# mobile flag
		"night_discon":False, 	# disable at weekdays 0:00-6:00 for CQU Huxi
		"interface":"wan0" 		# Warning: this interface value should be interface name as used in mwan3, rather than alias in luci
	},
	{
		"username":"2019xxxx",
		"password":"233333",
		"R6":"0",
		"night_discon":True,
		"interface":"wan1"
	}
]
tmp_file = "/tmp/drcom_result.txt"
#CONFIG END

def check_status(interface):# If you don't use mwan3, you should manually change this function.
	os.system("/usr/sbin/mwan3 status > {}".format(tmp_file))
	try:
		with open(tmp_file,'r',encoding='ascii',errors='ignore') as file:
			result = file.read()
			if result.find("interface {} is offline".format(interface)) != -1:
				return False
			else:
				return True
	except:
		return True


def do_login(username,password,interface,R6="0"):
	if R6 == "1":
		R6 = "1"
	else:
		R6 = "0"
	os.system("curl -m 10 --interface {} -H 'Uip: va5=1.2.3.4.' --resolve 'www.doctorcom.com:443:{}' https://www.doctorcom.com --data '0MKKey=0123456789&R6={}' --data-urlencode 'DDDDD={}' --data-urlencode 'upass={}' -k 1> /dev/null 2> /dev/null".format(interface,authserver,R6,username,password))

def write_pid():
	with open('/var/run/drcom.pid','w') as file:
		file.write(str(os.getpid()))

def watchdog():
	cold_start = True
	while True:
		for x in conn:
			if x['night_discon'] and (time()+8*60*60) % (24*60*60) < (6*60*60) and (strftime("%a",gmtime(time()+8*60*60)) not in ['Sat','Sun']):
				continue
			if not check_status(x['interface']):
				print("[INFO] {} attempt login {}:{}".format(asctime(localtime(time())),x['username'],x['R6']))
				do_login(x['username'],x['password'],x['interface'],x['R6'])
			else:
				if cold_start:
					print("[INFO] {} already logged in {}:{}".format(asctime(localtime(time())),x['username'],x['R6']))
		cold_start = False
		sleep(30)

def addiprule():
	# Avoid error caused by mwan3
	os.system("/sbin/ip rule del pref 100 to {} lookup main".format(authserver))
	os.system("/sbin/ip rule add pref 100 to {} lookup main".format(authserver))

addiprule()
write_pid()
watchdog()