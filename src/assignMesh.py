#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from salome2fish import *

s2f = salome2fish()


class assignMesh(QDialog):
    def __init__(self, parent=None, modal=0):
        QDialog.__init__(self, parent)
        self.setObjectName("Mesh")
        self.setModal(modal)
        self.setWindowTitle('Mesh')
        self.mesh_names = ''
        self.work_mesh = ''

    def setMeshNames(self, names):
        self.mesh_names = names

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.lb1 = QLabel('Mesh')

        self.le1 = QComboBox()
        self.le1.setEditable(True)
        self.le1.addItems(self.mesh_names)
        self.le1.setValidator(comboValidator(self.le1))
        self.le1.setCompleter(QCompleter(self.mesh_names))

        self.bt1 = QPushButton('Apply')
        self.bt1.clicked.connect(self.apply)

        grid.addWidget(self.lb1, 0, 0)
        grid.addWidget(self.le1, 0, 2)
        grid.addWidget(self.bt1, 0, 3)

        self.show()

    def apply(self):
        self.work_mesh = self.le1.currentText()
        self.work_mesh = self.work_mesh.encode(
            'unicode-escape').decode('string_escape')
        print (">>> Assigned mesh: " + self.work_mesh)
        print(type(self.work_mesh))
        s2f.set_work_mesh(self.work_mesh)
        print(s2f.mesh_assigned)


class comboValidator(QValidator):
    """Validator for editable combobox input field"""

    def __init__(self, combobox):
        super(QValidator, self).__init__(combobox)

    def validate(self, text, pos):
        """
        Validate the inputted text. Allow to enter the any item text only.

        Arguments:
        text (str): Validated text
        pos (int): Current position in editor

        Returns:
        (QValidator.State): Validation result state
        """
        state = QValidator.Invalid
        if len(text) == 0:
            state = QValidator.Intermediate
        else:
            idx = self.parent().findText(text, Qt.MatchStartsWith)
            if idx >= 0 and self.parent().itemText(idx).startswith(text):
                state = QValidator.Acceptable
        return state, text, pos
