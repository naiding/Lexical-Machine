
# -*- coding: utf-8 -*-   

import sys
import json
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4 import QtGui, QtCore
import LMConfig
import LMFileHelper
from Lexical_machine import LexicalMachine

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))  

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.machine = None
        self.config_style_dict = {}
        self.source_filename = None
        self.style_filename = None

        # Window Configuration
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.resize(screen.width(), screen.height())
        font = QFont(self.tr("Arial"),10)  
        QApplication.setFont(font)
        self.setWindowTitle(LMConfig.APPLICATION_NAME)
        self.setWindowIcon(QtGui.QIcon(LMConfig.APPLICATION_ICON))
        self.statusBar().showMessage('Ready')
        # QThread.sleep(1)

        # MenuBar Configuration
        self.configurate_menubar()

        self.set_opening_space()

    def configurate_menubar(self):
        self.configurate_file_menu()
        self.configurate_view_menu()
        self.configurate_run_menu()
        self.configurate_help_menu()

    def set_opening_space(self):
        # Launch Window Configuration
        self.OpenLabel = QtGui.QLabel( "Open a C Source File To Begin :)" )
        self.OpenLabel.setAlignment( QtCore.Qt.AlignCenter )
        self.OpenLabel.setFont(QFont("Arvo",13, QFont.Light))
        self.setCentralWidget(self.OpenLabel) 

    def set_working_space(self):
        # MainWindow Configuration
        self.mainSplitter = QSplitter(Qt.Horizontal,self)
        self.leftText = QTextBrowser(self.mainSplitter)  
        self.leftText.setAlignment(Qt.AlignCenter)  
        self.rightSplitter = QSplitter(Qt.Horizontal, self.mainSplitter)
        self.rightSplitter.setOpaqueResize(False)  
        self.upText = QTextBrowser(self.rightSplitter)  
        self.upText.setAlignment(Qt.AlignCenter)  
        self.bottomText = QTextBrowser(self.rightSplitter)  
        self.bottomText.setAlignment(Qt.AlignCenter)  
        self.mainSplitter.setStretchFactor(1,1)  
        self.mainSplitter.setWindowTitle(self.tr("分割窗口")) 
        self.setCentralWidget(self.mainSplitter)
        self.leftText.setFont(QFont("Consolas",12, QFont.Light))
        self.upText.setFont(QFont("Consolas",10, QFont.Light))
        self.bottomText.setFont(QFont("Consolas",10, QFont.Light))

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
        menubar_file.addSeparator()
        menubar_file.addAction(close_source_file)
        menubar_file.addAction(exit)  

    def open_a_source_file(self):
        self.source_filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Source File', '', 'Source Code(*.c)')
        self.setWindowTitle( self.source_filename + ' - ' + LMConfig.APPLICATION_NAME)
        self.set_working_space()
        self.machine = LexicalMachine(self.source_filename, self.style_filename)

        file_object = open(self.source_filename)
        try:
            all_the_text = file_object.read( )
            all_the_text = self.string2html(all_the_text)

            self.upText.setHtml("""
                <body>
                %s
                </body>
            """ % all_the_text)

        finally:
            file_object.close( )

    def string2html(self, all_the_text):
        all_the_text = all_the_text.replace("<", "&lt;")
        all_the_text = all_the_text.replace(">", "&gt;")
        all_the_text = all_the_text.replace("\n","<br>")
        all_the_text = all_the_text.replace(" ","&nbsp;")

        all_the_text = all_the_text.replace("include", """<font color=#800080>include</font>""")
        all_the_text = all_the_text.replace("int","""<font color=#000080>int</font>""")
        all_the_text = all_the_text.replace("long","""<font color=#000080>long</font>""")
        all_the_text = all_the_text.replace("double","""<font color=#000080>double</font>""")
        all_the_text = all_the_text.replace("float","""<font color=#000080>float</font>""")
        all_the_text = all_the_text.replace("char","""<font color=#000080>char</font>""")
        all_the_text = all_the_text.replace("short","""<font color=#000080>short</font>""")
        all_the_text = all_the_text.replace("if","""<font color=#6A5ACD>if</font>""")
        all_the_text = all_the_text.replace("else","""<font color=#6A5ACD>else</font>""")

        all_the_text = all_the_text.replace("for","""<font color=#800000>printf</font>""")
        all_the_text = all_the_text.replace("return","""<font color=#FF1493>return</font>""")
        all_the_text = all_the_text.replace("void","""<font color=#FF1493>void</font>""")
        all_the_text = all_the_text.replace("//","""<font color=#2E8B57>//</font>""")
        all_the_text = all_the_text.replace("{","""<font color=#Dc143c>{</font>""")
        all_the_text = all_the_text.replace("}","""<font color=#Dc143c>}</font>""")
        return all_the_text

    def open_a_style_file(self):
        self.style_filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Style File', '', 'Source Code(*.style)')
        self.machine = LexicalMachine(self.source_filename, self.style_filename)
        self.config_style_dict = self.machine.style


    def close_a_source_file(self):
        self.set_opening_space()
        print 'close'

    def configurate_view_menu(self):
        menubar = self.menuBar()
        menubar_view = menubar.addMenu('&View')

    def configurate_run_menu(self):

        # Run
        # CLOSE SOURCE FILE
        run_lexical_machine = QtGui.QAction(QtGui.QIcon(LMConfig.RUN_LEXICAL_MACHINCE_ICON), 
                                                     LMConfig.RUN_LEXICAL_MACHINCE_NAME, self)
        run_lexical_machine.setShortcut(LMConfig.RUN_LEXICAL_MACHINCE_SHORTCUT)
        run_lexical_machine.setStatusTip(LMConfig.RUN_LEXICAL_MACHINCE_STATUS)
        run_lexical_machine.triggered.connect(self.run)

        config_style = QtGui.QAction(QtGui.QIcon(LMConfig.CONFIG_STYLE_ICON),
                                                     LMConfig.CONFIG_STYLE_NAME, self)
        config_style.setShortcut(LMConfig.CONFIG_STYLE_SHORTCUT)
        config_style.setStatusTip(LMConfig.CONFIG_STYLE_STATUS)
        config_style.triggered.connect(self.config_style)

        menubar = self.menuBar()
        menubar_run = menubar.addMenu('&Run')
        menubar_run.addAction(run_lexical_machine)
        menubar_run.addAction(config_style)

    def configurate_help_menu(self):

        about = QtGui.QAction(QtGui.QIcon(LMConfig.ABOUT_ICON),
                                                     LMConfig.ABOUT_NAME, self)
        about.setShortcut(LMConfig.ABOUT_SHORTCUT)
        about.setStatusTip(LMConfig.ABOUT_STATUS)
        about.triggered.connect(self.about)

        menubar_help = self.menuBar()
        menubar_help = menubar_help.addMenu('&Help')
        menubar_help.addAction(about)

    def config_style(self):
        self.select_style_dialog = selectStyleWidget(self, self.config_style_dict)
        self.select_style_dialog.show()

    def about(self):
        self.about_us = QMessageBox()
        self.about_us.setWindowTitle('About us')
        self.about_us.resize(320, 240)
        self.about_us.setText("""Naiding Zhou:U201313768\nXuanyu Zheng:U201313768\nChenchen Xu:U201313768\n""")
        self.about_us.show()

    def run(self):
        print 'run'
        if self.source_filename == None or self.source_filename == '':
             QtGui.QMessageBox.information(self, "Empty Source File", "The source file can't be empty")
        else:
            try:
                self.machine = LexicalMachine(self.source_filename, self.style_filename)
                if  self.config_style_dict:
                    self.machine.style = self.config_style_dict
                self.machine.run()
            except Exception as e:
                QtGui.QMessageBox.information(self, "Failed!","Sorry, there is something wrong with the program." +
                                              "You can find information in the text browser")
                self.leftText.setText(e.message)
            else:
                QtGui.QMessageBox.information(self, "Success!",
                                              "The program runs successfully!\n" +
                                              "You can find the output file in {}\n".format(self.machine.output_filename) +
                                              "and the info file in {}".format(self.machine.output_info))
                self.leftText.setText(self.machine.info)
                file_object = open(self.machine.output_filename)
                try:
                    all_the_text = file_object.read( )
                    all_the_text = self.string2html(all_the_text)

                    self.bottomText.setHtml("""
                        <body>
                        %s
                        </body>
                    """ % all_the_text)
                finally:
                    file_object.close( )


class selectStyleWidget(QDialog):

    def __init__(self, mainWindow = None, configDict = None):

        super(QDialog, self).__init__()

        self.mainWindow = mainWindow
        self.configDict = configDict
        self.setWindowTitle(self.tr("Select Coding Style"))

        self.defaultLayout()

        if self.configDict:
            self.loadConfig()
        else:
            self.configDict = style_check(self.configDict)
            self.defaultConfig()

    def defaultLayout(self):
        self.TabStopLabel = QLabel(self.tr("TabStop:"))
        self.TabStopEdit = QSpinBox()
        self.TabStopEdit.setMinimum(0)
        self.TabStopEdit.setMaximum(16)

        self.SpecialCharacterLabel = QLabel(self.tr("""Special Characters:(split by ".")"""))
        self.SpecialCharacterEdit = QLineEdit()

        okButton = QPushButton(self.tr("Ok"))
        detailButton = QPushButton(self.tr("Detail >>"))
        self.connect(okButton,SIGNAL("clicked()"), self.ok)
        self.connect(detailButton,SIGNAL("clicked()"), self.showDetail)

        btnBox = QDialogButtonBox(Qt.Vertical)
        btnBox.addButton(okButton,QDialogButtonBox.ActionRole)
        btnBox.addButton(detailButton,QDialogButtonBox.ActionRole)

        baseLayout=QGridLayout()
        baseLayout.addWidget(self.TabStopLabel,0,0)
        baseLayout.addWidget(self.TabStopEdit,0,1)
        baseLayout.addWidget(okButton,0,3)
        baseLayout.addWidget(self.SpecialCharacterLabel,1,0)
        baseLayout.addWidget(self.SpecialCharacterEdit,1,1)
        baseLayout.addWidget(detailButton,1,3)

        self.check1 = QtGui.QCheckBox('left_parenthesis_newline')
        self.check2 = QtGui.QCheckBox('left_parenthesis_blank')
        self.check3 = QtGui.QCheckBox('left_parenthesis_right_blank')
        self.check4 = QtGui.QCheckBox('right_parenthesis_left_blank')
        self.check5 = QtGui.QCheckBox('brace_for_block')
        self.check6 = QtGui.QCheckBox('left_brace_new_line')
        self.check7 = QtGui.QCheckBox('delete_empty_statement')
        self.check8 = QtGui.QCheckBox('one_statement_per_line')

        self.detailWidget = QWidget()
        detailLayout=QGridLayout(self.detailWidget)
        detailLayout.addWidget(self.check1,1,0)
        detailLayout.addWidget(self.check2,2,0)
        detailLayout.addWidget(self.check3,3,0)
        detailLayout.addWidget(self.check4,4,0)
        detailLayout.addWidget(self.check5,5,0)
        detailLayout.addWidget(self.check6,6,0)
        detailLayout.addWidget(self.check7,7,0)
        detailLayout.addWidget(self.check8,8,0)

        self.detailWidget.hide()

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(baseLayout)
        mainLayout.addWidget(self.detailWidget)
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.setSpacing(10)

        self.setLayout(mainLayout)

    def defaultConfig(self):
        self.check5.setChecked(True)
        self.check6.setChecked(True)
        self.check7.setChecked(True)
        self.check8.setChecked(True)
        self.TabStopEdit.setValue(4)
        self.SpecialCharacterEdit.setText(',.;')


    def ok(self):

        if self.check1.isChecked():
            self.configDict['function']['left_parenthesis_newline'] = True
        else:
            self.configDict['function']['left_parenthesis_newline'] = False

        if self.check2.isChecked():
            self.configDict['function']['left_parenthesis_blank'] = True
        else:
            self.configDict['function']['left_parenthesis_blank'] = False

        if self.check3.isChecked():
            self.configDict['parenthesis']['left_parenthesis_right_blank'] = True
        else:
            self.configDict['parenthesis']['left_parenthesis_right_blank'] = False

        if self.check4.isChecked():
            self.configDict['parenthesis']['right_parenthesis_left_blank'] = True
        else:
            self.configDict['parenthesis']['right_parenthesis_left_blank'] = False

        if self.check5.isChecked():
            self.configDict['brace']['brace_for_block'] = True
        else:
            self.configDict['brace']['brace_for_block'] = False

        if self.check6.isChecked():
            self.configDict['brace']['left_brace_new_line'] = True
        else:
            self.configDict['brace']['left_brace_new_line'] = False

        if self.check7.isChecked():
            self.configDict['delete_empty_statement'] = True
        else:
            self.configDict['delete_empty_statement'] = False

        if self.check8.isChecked():
            self.configDict['one_statement_per_line'] = True
        else:
            self.configDict['one_statement_per_line'] = False

        self.configDict['tabstop'] = self.TabStopEdit.value()
        self.configDict['special_character_blank'] = unicode(self.SpecialCharacterEdit.text().toUtf8(), 'utf-8', 'ignore').split('.')
        self.mainWindow.config_style_dict = self.configDict
        self.close()

    def showDetail(self):
        if self.detailWidget.isHidden():
            self.detailWidget.show()
        else:
            self.detailWidget.hide()

    def loadConfig(self):

        self.check1.setChecked(self.configDict['function']['left_parenthesis_newline'])
        self.check2.setChecked(self.configDict['function']['left_parenthesis_blank'])
        self.check3.setChecked(self.configDict['parenthesis']['left_parenthesis_right_blank'])
        self.check4.setChecked(self.configDict['parenthesis']['right_parenthesis_left_blank'])
        self.check5.setChecked(self.configDict['brace']['brace_for_block'])
        self.check6.setChecked(self.configDict['brace']['left_brace_new_line'])
        self.check7.setChecked(self.configDict['delete_empty_statement'])
        self.check8.setChecked(self.configDict['one_statement_per_line'])

        self.TabStopEdit.setValue(self.configDict['tabstop'])
        self.SpecialCharacterEdit.setText('.'.join(self.configDict['special_character_blank']))

def style_check(self, dict = {}):
    # 4.1.1.1 Check the function and left parenthesis
    if dict.has_key('function'):
        if not dict['function'].has_key('left_parenthesis_blank'):
            dict['function']['left_parenthesis_blank'] = False
        if not dict['function'].has_key('left_parenthesis_newline'):
            dict['function']['left_parenthesis_newline'] = False
    else:
        dict['function'] = {
            'left_parenthesis_blank': False,
            'left_parenthesis_newline': False,
        }

    # 4.1.1.2 Check blank existence in the right of the left parenthesis
    # and the left of the right parenthesis
    if 'parenthesis' in dict:
        if not dict['parenthesis'].has_key('left_parenthesis_right_blank'):
            dict['parenthesis']['left_parenthesis_right_blank'] = False
        if not dict['parenthesis'].has_key('right_parenthesis_left_blank'):
            dict['parenthesis']['right_parenthesis_left_blank'] = False
    else:
        dict['parenthesis'] = {
            'left_parenthesis_right_blank': False,
            'right_parenthesis_left_blank': False,
        }

    # 4.1.1.3 tabstop, default is 4
    if not dict.has_key('tabstop'):
        dict['tabstop'] = 4

    # 4.1.1.4 blank character after special character
    if not dict.has_key('special_character_blank'):
        dict['special_character_blank'] = [',', ';']

    # 4.1.1.5 and 4.1.1.8
    # 4.1.1.5, 'brace_for_block' determine that no matter how many sentences
    #         in the block, there should always be braces
    # 4.1.1.8, 'left_brace_new_line', if it is true, then, the left brace should
    #         be in the new line
    if dict.has_key('brace'):
        if not dict['brace'].has_key('brace_for_block'):
            dict['brace']['brace_for_block'] = True
        if not dict['brace'].has_key('left_brace_new_line'):
            dict['brace']['left_brace_new_line'] = True
    else:
        dict['brace'] = {
            'brace_for_block': True,
            'left_brace_new_line': True,
        }

    # 4.1.1.6 'delete_empty_statement', it is true when empty statement should
    #         always be deleted
    if not dict.has_key('delete_empty_statement'):
        dict['delete_empty_statement'] = True

    # 4.1.1.7 'one_statement_per_line', every statement occupies one line
    if not dict.has_key('one_statement_per_line'):
        dict['one_statement_per_line'] = True

    return dict

app = QtGui.QApplication(sys.argv)

splash = QSplashScreen(QPixmap(LMConfig.APPLICATION_LAUNCH_IMAGE))  
splash.show()
app.processEvents()
main = MainWindow()
main.show()
splash.finish(main)  
sys.exit(app.exec_())

