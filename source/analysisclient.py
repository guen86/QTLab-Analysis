# Analysis client for QTLab
#
# Author: Wolfgang Pfaff <w.pfaff@tudelft.nl>
# Guenevere Prawiroatmodjo <g.e.d.k.prawiroatmodjo@tudelft.nl>

### Stuff we need to get cyclops up and running
import logging
l = logging.getLogger()
l.setLevel(logging.WARNING)

# make sure the userconfig is loaded
import os, sys
adddir = os.path.join(os.getcwd(), 'source')
sys.path.append(adddir)
sys.path.append(os.path.join(os.getcwd(), '..\\qtlab\\source\\'))
sys.path.append(os.path.join(os.getcwd(), '..\\qtlab\\source\\lib'))
sys.path.append(os.path.join(os.getcwd(), '..\\qtlab\\source\\lib\\gui'))
sys.path.append(os.getcwd() + '\\modules')
sys.path.insert(1,'c:\qtlab\source')

from lib.config import create_config
config = create_config('qtlabanalysis.cfg')

### some useful things that might get imported by other scripts
CONFIG_FILE = os.path.join(os.getcwd(), 'userconfig.py')

# load user config
if os.path.exists(CONFIG_FILE):
    execfile(CONFIG_FILE)
    
# we need this for ETS to work properly with pyqt
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtGui, QtCore

import time
import socket
import gobject
from lib.network.object_sharer import helper
from lib.network.tcpserver import GlibTCPHandler
PORT = 12002

# methods/classes for QT4 clients that replace the glib-based ones
class QtTCPHandler(GlibTCPHandler, QtCore.QObject):
    def __init__(self, sock, client_address, server, packet_len=False):
        QtCore.QObject.__init__(self)
        GlibTCPHandler.__init__(self, sock, client_address, server, packet_len)

        self.socket_notifier = QtCore.QSocketNotifier(\
            self.socket.fileno(), QtCore.QSocketNotifier.Read)
        self.socket_notifier.setEnabled(True)
        self.socket_notifier.activated.connect(self._socketwatcher_recv)
        
    def enable_callbacks(self):
        return

    def disable_callbacks(self):
        return

    # @QtCore.pyqtSlot()
    def _socketwatcher_recv(self, *args):
        self._handle_recv(self.socket, gobject.IO_IN)

# class QtTCPHandler
class _QtDummyHandler(QtTCPHandler):
    def __init__(self, sock, client_address, server):
        QtTCPHandler.__init__(self, sock, client_address, server,
                packet_len=True)
        helper.add_client(self.socket, self)

    def handle(self, data):
        if len(data) > 0:
            data = helper.handle_data(self.socket, data)
        return True

# class _QtDummyHandler

# here we go...
if __name__ == "__main__":

    # start our main application
    qtlabanalysis_app = QtGui.QApplication(sys.argv)
    
    # open the socket and start the client.
    # will fail if no connection to qtlab is available   
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((config['ip'], PORT))    
    handler = _QtDummyHandler(sock, 'client', 'server')
    
    from plotwin import PlotWin
    plotwindow = PlotWin()
    plotwindow.show()
    sys.exit(qtlabanalysis_app.exec_())