#!/usr/bin/python
# PYTHON_ARGCOMPLETE_OK

"""
  SSH rsa keys

  RCS-ID:      $Id: ssh-manager.py, v0.1 20.08.2019 18:29 Worked Exp $
  Author:      Worked <operador@gmail.com>
  Created:     20.08.2019 v0.1 ssh-manager.py
  License:     GNU General Public License v3.0 

  That Python file is free software; you can redistribute it and/or modify it
  under the terms of the GNU General Public License as published by the Free
  Software Foundation; either version 2 of the License, or (at your option)
  any later version.

  That Python file is distributed in the hope that it will be, useful but
  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
  for more details.

  You should have received a copy of the GNU General Public License
  along with Windows Live Messenger Class; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import argcomplete
import argparse
from os import listdir, system
from os.path import isfile, join

def get_rsa_enabled(prefix, parsed_args, **kwargs):
    """
    Return all rsa keys enabled for autocomplete option
    """
    rsas = [f for f in listdir('/etc/ssh/keys-enabled/') if isfile(join('/etc/ssh/keys-enabled/', f))]
    return rsas
# - --  ---   ------------------------------------------------------------

def get_rsa_available(prefix, parsed_args, **kwargs):
    """
    Return all rsa keys available for autocomplete option
    """
    rsas = [f for f in listdir('/etc/ssh/keys-available/') if isfile(join('/etc/ssh/keys-available/', f))]
    return rsas
# - --  ---   ------------------------------------------------------------

class authorize:
    """
    Creacion del archivo /root/.ssh/authorized_keys de forma rapida y sencilla con los
    patrones de keys disponibles y keys habilitadas introducido por apache2.
    """
    def __init__(self, args):
        # Variables de uso interno
        self.enabled = '/etc/ssh/keys-enabled/'
        self.available = '/etc/ssh/keys-available/'
        self.restore = args.restore
        self.install = args.install
        self.install_all = args.install_all
        self.remove = args.remove
        self.remove_all = args.remove_all

    def rsa_install(self, rsa):
        if isfile(join(self.enabled, rsa)):
            return '%s YA esta instalada.' % rsa
        elif not isfile(join(self.available, rsa)):
            return '%s NO esta disponible.' % rsa
        else:
            system('ln -s %s%s %s%s' % (self.available, rsa, self.enabled, rsa))
            print 'ssh-manager: ssh-rsa %s key instalada correctamente.' % rsa
            return self.rsa_restore()

    def rsa_install_all(self):
        rsas = [f for f in listdir(self.available) if isfile(join(self.available, f))]
        for key in rsas:
            if not isfile(join(self.enabled, key)):
                system('ln -s %s%s %s%s' % (self.available, key, self.enabled, key))
        return self.rsa_restore()

    def rsa_remove(self, rsa):
        if not isfile(join(self.enabled, rsa)):
            return '%s NO esta instalada.' % rsa
        else:
            system('rm %s%s' % (self.enabled, rsa))
            print 'ssh-manager: ssh-rsa %s key eliminada correctamente.' % rsa
            return self.rsa_restore()

    def rsa_remove_all(self):
        rsas = [f for f in listdir(self.enabled) if isfile(join(self.enabled, f))]
        for key in rsas:
            system('rm %s%s %s%s' % (self.enabled, key))
        return self.rsa_restore()

    def rsa_restore(self):
        rsas = [f for f in listdir(self.enabled) if isfile(join(self.enabled, f))]
        system('rm /root/.ssh/authorized_keys')
        if len(rsas) > 0:
            for key in rsas:
                system('cat %s%s >> /root/.ssh/authorized_keys' % (self.enabled, key))
            return '%d ssh-rsa keys restauradas.' % len(rsas)
        else:
            return 'NO existen ssh-rsa keys que restaurar.'

    def __repr__(self):
        if self.install:
            return self.rsa_install(self.install)
        elif self.install_all:
            return self.rsa_install_all()
        elif self.remove:
            return self.rsa_remove(self.remove)
        elif self.remove_all:
            return self.rsa_remove_all()
        elif self.restore:
            return self.rsa_restore()
# - --  ---   ------------------------------------------------------------

""" Command line parser
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog='ssh-manager',
            description='''Restauracion de ssh-rsa keys en /root/.ssh/authorized_keys.\
                        Actualmente este script cuenta con autocompletado que mostrara\
                        las keys disponibles (--install) y las instaladas (--remove)\
                        al tabular una vez escrita la orden, siendo de esta forma mas\
                        intuitivo de cara al usuario.''',
            epilog='always use ssh-manager, make your day over ssh more simple.')

    # Comandos aceptados
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--restore', action='store_true', help='restaura las rsa keys de /etc/ssh/keys-enabled/')
    group.add_argument('--install', metavar='file', help='activa una rsa key').completer = get_rsa_available
    group.add_argument('--install-all', action='store_true', help='activa las rsa keys de /etc/ssh/keys-available/')
    group.add_argument('--remove', metavar='file', help='elimina una rsa key activa').completer = get_rsa_enabled
    group.add_argument('--remove-all', action='store_true', help='elimina las rsa keys de /etc/ssh/keys-enabled/')

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    # Iniciamos el autocompleter
    argcomplete.autocomplete(parser)

    # Iniciamos el parser
    args = parser.parse_args()

    # Debugueo del bueno y rico
    #print args

    # Magia que comienza aqui....
    print 'ssh-manager: %s' % authorize(args)
