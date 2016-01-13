# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class selectStyleWidget(QDialog):

    def __init__(self, parent = None):
        super(QDialog, self).__init__(parent)
        self.setWindowTitle(self.tr("Select Coding Style"))

        self.TabStopLabel = QLabel(self.tr("TabStop:"))
        self.TabStopEdit = QSpinBox()
        self.TabStopEdit.setValue(4)
        self.TabStopEdit.setMinimum(0)
        self.TabStopEdit.setMaximum(16)

        self.SpecialCharacterLabel = QLabel(self.tr("""Special Characters:(split by ",")"""))
        self.SpecialCharacterEdit = QLineEdit()
        self.SpecialCharacterEdit.setText(',,;')

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

        self.check5.setChecked(True)
        self.check6.setChecked(True)
        self.check7.setChecked(True)
        self.check8.setChecked(True)


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

    def ok(self):
        print 'ok'

    def showDetail(self):
        if self.detailWidget.isHidden():
            self.detailWidget.show()
        else:
            self.detailWidget.hide()

# app=QApplication(sys.argv)
# main = Extension()
# main.show()
# app.exec_()