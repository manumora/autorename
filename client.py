#!/usr/bin/env python
##############################################################################
# -*- coding: utf-8 -*-
# Project:     Autorename
# Module:      client.py
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

import sys, os, socket, time, shutil, xmlrpclib

loginsToRename=10
lastLogin=sys.argv[1]

loginsDir="/var/lib/autorename-client"
loginsFile=loginsDir+"/userlogins"
log="/var/log/autorename-client.log"

if not os.path.isdir(loginsDir):
	os.mkdir(loginsDir)

# Escribimos el ultimo logueo
f = open(loginsFile,"a")
f.write(lastLogin+"\n")
f.close()

# Obtenemos los ultimos x logueos
f = open(loginsFile,"r")
f.seek(0,2)
fsize = f.tell()
f.seek (max (fsize-1024, 0), 0)
listLastLogins = f.readlines()[-loginsToRename:]
f.close()

# Le quitamos los saltos de linea
for x, i in enumerate(listLastLogins):
	listLastLogins[x]=i.replace("\n","")

hostname = socket.gethostname()

# Si hay al menos x logins, todos son del ultimo usuario logueado
# y el nombre del equipo se llama de una forma diferente, renombramos
if len(listLastLogins)>=loginsToRename and listLastLogins.count(lastLogin)==loginsToRename and lastLogin!=hostname:

	# Comprobamos que haya comunicacion con el Servidor
	try:
		server = xmlrpclib.ServerProxy("http://servidor:9997")
		server.ping()
	except:
		exit()

	newHostname = lastLogin

	f = open("/etc/hostname","w")
	f.write(newHostname)
	f.close()

	f = open("/etc/hosts","w")
	f.write("127.0.0.1	localhost\n")
	f.write("127.0.1.1	"+newHostname+"\n\n")
	f.write("# The following lines are desirable for IPv6 capable hosts\n")
	f.write("::1	localhost ip6-localhost ip6-loopback\n")
	f.write("fe00::0 ip6-localnet\n")
	f.write("ff00::0 ip6-mcastprefix\n")
	f.write("ff02::1 ip6-allnodes\n")
	f.write("ff02::2 ip6-allrouters")
	f.close()

	os.system("hostname -F /etc/hostname")

	# Obtenemos el numero de serie de la maquina
	f = open("/sys/class/dmi/id/product_serial","r")
	serialNumber = f.read().replace("\n","")
	f.close()

	# Se lo comunicamos al servidor para que borre los certificados
	try:
		server.removeCerts(hostname, newHostname)
		server.setLog(hostname+"#"+newHostname+"#"+serialNumber)
	except:
		pass

	# Borramos los certificados locales y reiniciamos puppet
	if os.path.isdir("/var/lib/puppet/ssl"):
		shutil.rmtree("/var/lib/puppet/ssl")
	os.system("/etc/init.d/puppet restart")

	# Guardamos en el log
	f = open(log,"a")
	f.write(hostname+"#"+newHostname+"#"+serialNumber+"#"+time.strftime("%Y-%m-%d %H:%M:%S")+"\n")
	f.close()
