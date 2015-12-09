
# -*- coding: utf-8 -*-   

import sys
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
  

from PyQt4 import QtGui, QtCore
import LMConfig

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Window Configuration
        self.resize(640, 320)
        font = QFont(self.tr("Arial"),10)  
        QApplication.setFont(font)  
        self.setWindowTitle(LMConfig.APPLICATION_NAME)
        self.setWindowIcon(QtGui.QIcon(LMConfig.APPLICATION_ICON))
        self.statusBar().showMessage('Ready')
        QThread.sleep(1)  

        # MenuBar Configuration
        self.configurate_menubar()

        self.OpenLabel = QtGui.QLabel( "Open a C Source File To Begin :)" )
        self.OpenLabel.setAlignment( QtCore.Qt.AlignCenter )
        self.OpenLabel.setFont(QFont("Arvo",13, QFont.Light))
        self.setCentralWidget(self.OpenLabel)


    def configurate_menubar(self):
        self.configurate_file_menu()
        self.configurate_view_menu()
        self.configurate_run_menu()
        self.configurate_help_menu()

    def configurate_file_menu(self):

        # OPEN SOURCE FILE
        open_source_file = QtGui.QAction(QtGui.QIcon(LMConfig.OPEN_SOURCE_FILE_ICON), 
                                                     LMConfig.OPEN_SOURCE_FILE_NAME, self)
        open_source_file.setShortcut(LMConfig.OPEN_SOURCE_FILE_SHORTCUT)
        open_source_file.setStatusTip(LMConfig.OPEN_SOURCE_FILE_STATUS)
        open_source_file.triggered.connect(self.open_a_source_file)

        # OPEN STYLE FILE
        open_style_file = QtGui.QAction(QtGui.QIcon(LMConfig.OPEN_STYLE_FILE_ICON), 
                                                     LMConfig.OPEN_STYLE_FILE_NAME, self)
        open_style_file.setShortcut(LMConfig.OPEN_STYLE_FILE_SHORTCUT)
        open_style_file.setStatusTip(LMConfig.OPEN_STYLE_FILE_STATUS)
        open_style_file.triggered.connect(self.open_a_style_file)

        # SAVE OUTPUT INFO
        save_output_info = QtGui.QAction(QtGui.QIcon(LMConfig.SAVE_OUTPUT_INFO_ICON), 
                                                     LMConfig.SAVE_OUTPUT_INFO_NAME, self)
        save_output_info.setShortcut(LMConfig.SAVE_OUTPUT_INFO_SHORTCUT)
        save_output_info.setStatusTip(LMConfig.SAVE_OUTPUT_INFO_STATUS)
        save_output_info.triggered.connect(self.save_info_to_file)

        # SAVE OUTPUT FILE
        save_output_file = QtGui.QAction(QtGui.QIcon(LMConfig.SAVE_OUTPUT_FILE_ICON), 
                                                     LMConfig.SAVE_OUTPUT_FILE_NAME, self)
        save_output_file.setShortcut(LMConfig.SAVE_OUTPUT_FILE_SHORTCUT)
        save_output_file.setStatusTip(LMConfig.SAVE_OUTPUT_FILE_STATUS)
        save_output_file.triggered.connect(self.save_output_to_file)

        # CLOSE SOURCE FILE
        close_source_file = QtGui.QAction(QtGui.QIcon(LMConfig.CLOSE_SOURCE_FILE_ICON), 
                                                     LMConfig.CLOSE_SOURCE_FILE_NAME, self)
        close_source_file.setShortcut(LMConfig.CLOSE_SOURCE_FILE_SHORTCUT)
        close_source_file.setStatusTip(LMConfig.CLOSE_SOURCE_FILE_STATUS)
        close_source_file.triggered.connect(self.close_a_source_file)

        # EXIT
        exit = QtGui.QAction(QtGui.QIcon(LMConfig.EXIT_APPLICATION_ICON),
                                         LMConfig.EXIT_APPLICATION_NAME, self)
        exit.setShortcut(LMConfig.EXIT_APPLICATION_SHORTCUT)
        exit.setStatusTip(LMConfig.EXIT_APPLICATION_STATUS)
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        menubar = self.menuBar()
        menubar_file = menubar.addMenu('&File')
        menubar_file.addAction(open_source_file)
        menubar_file.addAction(open_style_file)
        menubar_file.addSeparator()
        menubar_file.addAction(save_output_info)
        menubar_file.addAction(save_output_file)
        menubar_file.addSeparator()
        menubar_file.addAction(close_source_file)
        menubar_file.addAction(exit)  

    def open_a_source_file(self):
        self.source_filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Source File', '', 'Source Code(*.c)')
        self.setWindowTitle( self.source_filename + ' - ' + LMConfig.APPLICATION_NAME)
        self.OpenLabel.setVisible(False)

    def open_a_style_file(self):
        self.style_filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Style File', '', 'Source Code(*.style)')

    def save_info_to_file(self):
        print 'save info'

    def save_output_to_file(self):
        print 'save output'

    def close_a_source_file(self):
        print 'close'

    def configurate_view_menu(self):
        menubar = self.menuBar()
        menubar_view = menubar.addMenu('&View')

    def configurate_run_menu(self):
        menubar = self.menuBar()
        menubar_run = menubar.addMenu('&Run')

    def configurate_help_menu(self):
        menubar = self.menuBar()
        menubar_help = menubar.addMenu('&Help')


app = QtGui.QApplication(sys.argv)

splash = QSplashScreen(QPixmap(LMConfig.APPLICATION_LAUNCH_IMAGE))  
splash.show()  
app.processEvents()  
main = MainWindow()
main.show()
splash.finish(main)  
sys.exit(app.exec_())