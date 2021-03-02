#!/bin/sh /etc/rc.common
# This script used for /etc/init.d script, you can use it to running as a service on OpenWRT
START=99
STOP=15

start() {
  /usr/bin/python3 /usr/drcom.py &
}

stop() {
  kill -9 `cat /var/run/drcom.pid`
}
