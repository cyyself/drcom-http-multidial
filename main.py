#!/usr/bin/env python3
import os
from time import *
#CONFIG BEGIN
authserver = "202.202.0.163"
# 202.202.0.163 for CQU Campus A and B, 10.254.7.4 for CQU Campus D (Huxi)
conn = [
	{
		"username":"2018xxxx",
		"password":"233333",#If there is ' in your password, you should manually escape
		"R6":"0",#mobile flag
		"bind": {#This is an option for multidial, for single connection, no bind is ok
			"interface":"eth0",
			"ip":"172.20.233.66",
			"gateway":"172.20.233.1"
		}
	}
]
tmp_file = "/tmp/drcom_result.txt"
#CONFIG END

def clear_route():
	os.system("ip route delete {} 1> /dev/null 2> /dev/null".format(authserver))

def switch_route(thisConn):
	if (not 'bind' in thisConn):
		return
	clear_route()
	interface = thisConn['bind']['interface']
	ip = thisConn['bind']['ip']
	gateway = thisConn['bind']['gateway']
	os.system("ip route add {} via {} src {} dev {}".format(authserver,gateway,ip,interface))

def check_status(username):
	os.system("curl http://{} 1> {} 2> /dev/null".format(authserver,tmp_file))
	with open(tmp_file,'r',encoding='ascii',errors='ignore') as file:
		result = file.read()
		if result.find("uid='{}'".format(username)) != -1:
			return True
	return False

def do_login(username,password,R6="0"):
	if R6:
		R6 = "1"
	else:
		R6 = "0"
	os.system("curl -H 'Uip: va5=1.2.3.4.' --resolve 'www.doctorcom.com:443:{}' https://www.doctorcom.com --data '0MKKey=0123456789&R6={}' --data-urlencode 'DDDDD={}' --data-urlencode 'upass={}' -k 1> /dev/null 2> /dev/null".format(authserver,R6,username,password))

def watchdog():
	while True:
		for x in conn:
			switch_route(x)
			if not check_status(x['username']):
				print("[INFO] {} attempt login {}".format(asctime(localtime(time())),x['username'],x['R6']))
				do_login(x['username'],x['password'],x['R6'])
				if check_status(x['username']):
					print("[INFO] {} succeed {}".format(asctime(localtime(time())),x['username'],x['R6']))
				else:
					print("[ERROR] {} failed {}".format(asctime(localtime(time())),x['username'],x['R6']))
			clear_route()
		sleep(300)

watchdog()
