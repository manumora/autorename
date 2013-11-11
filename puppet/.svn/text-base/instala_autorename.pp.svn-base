##############################################################################
# Project:     Autorename
# Purpose:     Puppet task
# Date:        23-May-2012.
# Author:      Manuel Mora Gordillo
# Copyright:   2012 - Manuel Mora Gordillo    <manuel.mora.gordillo @nospam@ gmail.com>
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

class instala_autorename {

 file { "/var/cache/autorename-client_0.1-12_all.deb":
          owner => root, group => root, mode => 644,
          source => "puppet://puppetinstituto/files/autorename-client_0.1-12_all.deb"
 }

 exec { "instalar_paquete_autorename" :
      path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
      command => "dpkg -i /var/cache/autorename-client_0.1-12_all.deb",
      unless => "dpkg -l autorename-client | grep ii | grep 0.1-12",
      require  => File["/var/cache/autorename-client_0.1-12_all.deb"]
 }
}

