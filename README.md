##############################################################################
# Project:     Autorename
# Purpose:     Autorename of laptops
# Language:    Python 2.5
# Date:        23-Apr-2012.
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

Descripción
En el cambio de curso escolar se hace imprescindible la reasignación de portátiles
de unos alumnos a otros. Cada equipo se nombra con el username del alumno por lo 
que al reasignar el portátil hay que renombrar el equipo.
Para aumentar la productividad del Administrador Informático se requieren automatizar 
algunos procesos. El motivo de este software es el autorenombrado del portátil sin
ser necesaria la intervención del Administrador Informático.

Información técnica
Paquetes:
	- autorename-client: Hay que instalarlo en los portátiles. Registra cada autenticación
	de usuario y renombra el equipo si se cumplen cuatro condiciones:
		* Al menos hay 10 autenticaciones de usuario
		* Las últimas 10 autenticaciones tienen que ser del mismo usuario
		* El equipo se llama de forma diferente al username de las últimas autenticaciones
		* Hay conexión con el Servidor NFS
	Si el autorenombrado se ha llevado a cabo se lo comunica al Servidor NFS

	- autorename-server: Hay que instalarlo en el servidor NFS. Está a la escucha y borra los
	certificados puppet cuando un portátil es renombrado.

Ficheros:
	- autorename-client:
		* /etc/gdm/PostLogin/Default: ejecuta client.py cuando un usuario se ha autenticado
		pasándole como parámetro el username
		* /usr/share/autorename-client/client.py: el script que realiza todo el proceso
		* /var/lib/autorename-client/userlogin: donde se registran las autenticaciones de usuario
		* /var/log/autorename-client.log: cuando un equipo es renombrado se registra con el
		siguiente formato: nombre_actual#nuevo_nombre#fecha_hora

	- autorename-server:
		* /usr/share/autorename-server/server.py: script que realiza el proceso de escucha y
		borrado de certificados puppet
		* /etc/init.d/autorename: demonio del script server.py
		* /var/log/autorename-server.log: registra cuando un equipo se ha renombrado con el
		siguiente formato: nombre_actual#nuevo_nombre#numero_serie#fecha_hora

