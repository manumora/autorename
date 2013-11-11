#!/usr/bin/env python
##############################################################################
# -*- coding: utf-8 -*-
# Project:     Autorename
# Module:      server.py
# Purpose:     Autorename for laptops
# Language:    Python 2.5
# Date:        23-Apr-2012.
# Ver:         23-Apr-2012.
# Author:      Manuel Mora Gordillo
# Copyright:   2012 - Manuel Mora Gordillo    <manuito @nospam@ gmail.com>
#
# Autorename is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# Autorename is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Autorename. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from SimpleXMLRPCServer import SimpleXMLRPCServer
import socket, os, time

def getDomain():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	dom ='sindominio'
	try:
		s.connect(("servidor", 0))
		inet_address= s.getsockname()[0]
		nombre=socket.gethostbyname_ex(socket.gethostname())[0].split(".")
		if len(nombre)>1:
			dom=nombre[1]
	except:
		pass

	return dom

def ping():
	return "pong"

def removeCerts (hostname, newHostname):
	os.system("puppetca --clean "+hostname)
	os.system("puppetca --clean "+hostname+"."+getDomain())
	os.system("rm -f /var/lib/puppet/yaml/node/"+hostname+".*")
	os.system("rm -f /var/lib/puppet/yaml/facts/"+hostname+".*")
	os.system("puppetca --clean "+newHostname)
	os.system("puppetca --clean "+newHostname+"."+getDomain())
	os.system("rm -f /var/lib/puppet/yaml/node/"+newHostname+".*")
	os.system("rm -f /var/lib/puppet/yaml/facts/"+newHostname+".*")

	return True

def setLog(text):
	log="/var/log/autorename-server.log"
	f = open(log,"a")
	f.write(text+"#"+time.strftime("%Y-%m-%d %H:%M:%S")+"\n")
	f.close()

server = SimpleXMLRPCServer (("servidor", 9997))
server.register_function (removeCerts)
server.register_function (ping)
server.register_function (setLog)
server.serve_forever ()
