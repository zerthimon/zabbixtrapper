# -*- coding: utf-8 -*-
# Zabbix Trapper Python interface library - zabbixtrapper.py
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; only version 2 of the License is applicable.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#
# Author: 
#     Lior Goikhburg <goikhburg at gmail.com >
#
# Description:
#     This library is used to send traps to Zabbix
#
# Zabbix:
#     http://www.zabbix.com

import socket
import struct
import json


class ZabbixError(Exception):
        pass


class ServerError(Exception):
        pass


class ZabbixTrapper(object):
    def __init__(self, host, port, timeout = 10):
        self.host = host
        self.port = int(port)
        self.timeout = timeout
        self._socket = None

    def _connect(self):
        """
        Connects to zabbix trapper port
        """

        if self._socket is not None:
            return
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(self.timeout)
            self._socket.connect((self.host, self.port))
        except socket.error as error:
            self._disconnect()
            if len(error.args) == 1:
                raise ServerError("Error connecting to Zabbix on %s:%s: %s:" % (self.host,
                                                                                self.port,
                                                                                error.args[0]))
            else:
                raise ServerError("Error %s connecting to Zabbix on %s:%s: %s" % (error.args[0],
                                                                                  self.host,
                                                                                  self.port,
                                                                                  error.args[1]))

    def _disconnect(self):
        """
        Disconnects from zabbix trapper port
        """

        if self._socket:
            try:
                self._socket.close()
            except socket.error:
                pass
            finally:
                self._socket = None

    def _write_data(self, data):
        """
        Writes data to socket
        """

        data_length = struct.pack('<Q', len(data))
        request = 'ZBXD\1' + data_length + data
        try:
            self._socket.sendall(request)
        except socket.error as error:
            self._disconnect()
            if len(error.args) == 1:
                raise ServerError("Error sending data to Zabbix on %s:%s: %s:" % (self.host,
                                                                                  self.port,
                                                                                  error.args[0]))
            else:
                raise ServerError("Error %s sending data to Zabbix on %s:%s: %s" % (error.args[0],
                                                                                  self.host,
                                                                                  self.port,
                                                                                  error.args[1]))

    def _read_data(self):
        """
        Reads data from socket according to protocl
        """

        # read response header (13 bytes)
        resp_hdr = self._read_sock(self._socket, 13)
        if not resp_hdr.startswith('ZBXD\1') or len(resp_hdr) != 13:
            raise ZabbixError('Wrong Zabbix Response')

        # body lengh comes after 5'th byte
        resp_body_len = struct.unpack('<Q', resp_hdr[5:])[0]
        resp_body = self._read_sock(self._socket, resp_body_len)
        return resp_body

    def _read_sock(self, sock, count):
        """
        Buffered reading from socket
        """

        buf = ''
        try: 
            while len(buf)<count:
                chunk = sock.recv(count-len(buf))
                if not chunk:
                    return buf
                buf += chunk
        except socket.error as error:
            self._disconnect()
            if len(error.args) == 1:
                raise ServerError("Error receiving data from Zabbix on %s:%s: %s:" % (self.host,
                                                                                      self.port,
                                                                                      error.args[0]))
            else:
                raise ServerError("Error %s sending data to Zabbix on %s:%s: %s" % (error.args[0],
                                                                                    self.host,
                                                                                    self.port,
                                                                                    error.args[1]))
        return buf

    def send_data(self, data):
        """
        Connects, sends request, reads response, disconnects, returns response
        """

        self._connect()
        self._write_data(data)
        response = self._read_data()
        self._disconnect()
        return response

    def send_traps(self, traps):
        """
        Converts data to json and sends to zabbix, receives data from zabbix and returns as json
        """

        message = json.dumps({'request': 'sender data', 'data': traps})
        result = json.loads(self.send_data(message))
        return result
