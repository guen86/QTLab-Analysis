# The Cyclops main window
#
# Author: Wolfgang Pfaff <w.pfaff@tudelft.nl>

import os, sys
import ConfigParser
from PyQt4 import QtCore, QtGui, Qt
from lib import config as _cfg
from ui_main_window import Ui_mainWindow
from panel import Panel, PanelDialog

# some constants
PANEL_CFG = 'cyclops_panels.py'
GEOMETRY_CFG = 'cyclops_geometry.cfg'

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # import designer interface
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        # load the user panel config
        self.load_user_panels()

        # set full screen
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # restore saved state
        self._load_config()
 
    def add_panel(self, panel, *arg, **kw):
        p = PanelDialog(panel, *arg, **kw)
        new_window = self.ui.mdiArea.addSubWindow(p)
        new_window.setAttribute(Qt.Qt.WA_DeleteOnClose)
        new_window.show()

    def load_user_panels(self):
        """
        Loads the user script in which the start-up panel configuration
        is specified.
        """
        add_panel = self.add_panel

        # process the command line args. try to load anything as panel config that
        # ends with .py. if there's no such thing, load the default user config
        args = 0
        for f in sys.argv[1:]:
            if f[-3:] == '.py':
                args += 1
                execfile(f)
        if args == 0:
            execfile(os.path.join(os.getcwd(),PANEL_CFG))

    
    def closeEvent(self, event):
        self._write_config()
   
    def _write_config(self, geometry_cfg_file=GEOMETRY_CFG):
        config = ConfigParser.RawConfigParser()

        # mainwindow geometry
        try:
            config.add_section('mainwindow')
            config.set('mainwindow', 'w', self.width())
            config.set('mainwindow', 'h', self.height())
        except:
            pass

        # subwindow geometries
        for w in self.ui.mdiArea.subWindowList():
            try:
                t = str(w.windowTitle())
                config.add_section(t)
                config.set(t, 'x', w.x())
                config.set(t, 'y', w.y())
                config.set(t, 'w', w.width())
                config.set(t, 'h', w.height())
                config.set(t, 'shaded', w.isShaded())
                config.set(t, 'minimized', w.isMinimized())
            except:
                pass

        # write to file
        with open(geometry_cfg_file, 'wb') as configfile:
            config.write(configfile)
        

    def _load_config(self, geometry_cfg_file=GEOMETRY_CFG):
        config = ConfigParser.RawConfigParser()
        config.read(geometry_cfg_file)

        # mainwindow geometry;
        try:
            h, w = config.getint('mainwindow', 'h'), \
                config.getint('mainwindow', 'w')
            self.setGeometry(5, 15, w, h)
        except:
            pass

        # subwindow geometries
        windows = {}
        for w in self.ui.mdiArea.subWindowList():
            windows[str(w.windowTitle())] = w

        for s in config.sections():
            if s != 'mainwindow' and s in windows:
                try:
                    x, y = config.getint(s, 'x'), config.getint(s, 'y')
                    w, h = config.getint(s, 'w'), config.getint(s, 'h')
                    shaded = config.getboolean(s, 'shaded')
                    minimized = config.getboolean(s, 'minimized')
                    windows[s].setGeometry(x,y,w,h)
                    if shaded: windows[s].showShaded()
                    if minimized: windows[s].showMinimized()
                except:
                    pass
                

        
        
