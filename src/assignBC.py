#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np


class assignBC(QDialog):
    def __init__(self, parent=None, modal=0):
        QDialog.__init__(self, parent)
        self.setObjectName("BoundaryCondition")
        self.setModal(modal)
        self.setWindowTitle('BoundaryCondition')
        self.type = ['x+', 'x-', 'y+', 'y-', 'z+',
                     'z-', 'Inclined plane', 'curved surface']
        self.type_ID = [1, -1, 2, -2, 3, -3, 4, 5]
        self.cond = ['vacuum', 'reflect']
        self.cond_ID = [0, 1]
        self.names = []

    def get_type_ID(self, type):
        if (type == 'x+'):
            return 1
        if (type == 'x-'):
            return -1
        if (type == 'y+'):
            return 2
        if (type == 'y-'):
            return -2
        if (type == 'z+'):
            return 3
        if (type == 'z-'):
            return -3
        if (type == 'Inclined plane'):
            return 4
        if (type == 'curved surface'):
            return 5

    def get_cond_ID(self, cond):
        if (cond == 'vacuum'):
            return 0
        if (cond == 'reflect'):
            return 1

    def setBoundaryNames(self, names):
        self.names = names
        self.nb = len(self.names)
        self.bt_idx = np.zeros((self.nb), dtype=np.int64)
        self.bc_idx = np.zeros((self.nb), dtype=np.int64)

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.lb1 = QLabel('Boundary')
        self.lb2 = QLabel('Type')
        self.lb3 = QLabel('Condition')

        # self.le2 = QComboBox()
        # self.le2.setEditable(True)
        # self.le2.addItems(self.type)
        # self.le2.setValidator(comboValidator(self.le2))
        # self.le2.setCompleter(QCompleter(self.type))

        # self.le3 = QComboBox()
        # self.le3.setEditable(True)
        # self.le3.addItems(self.cond)
        # self.le3.setValidator(comboValidator(self.le3))
        # self.le3.setCompleter(QCompleter(self.cond))

        self.bt1 = QPushButton('Apply')
        self.bt1.clicked.connect(self.apply)

        grid.addWidget(self.lb1, 0, 0)
        grid.addWidget(self.lb2, 0, 1)
        grid.addWidget(self.lb3, 0, 3)
        grid.addWidget(self.bt1, self.nb, 4)

        le_names = locals()
        le_names1 = locals()
        self.list2 = []
        self.list3 = []
        for i in range(self.nb):
            lb = QLabel(self.names[i])
            grid.addWidget(lb, i + 1, 0)

            le_names['n' + str(i + 2)] = 'self.le' + str(i + 2)
            self.list2.append(eval('n{}'.format(i + 2)))
            self.list2[i] = QComboBox()
            self.list2[i].setEditable(True)
            self.list2[i].addItems(self.type)
            self.list2[i].setValidator(comboValidator(self.list2[i]))
            self.list2[i].setCompleter(QCompleter(self.type))
            grid.addWidget(self.list2[i], i + 1, 1)

            le_names1['n' + str(self.nb + i + 2)] = 'self.le' + \
                str(self.nb + i + 2)
            self.list3.append(eval('n{}'.format(self.nb + i + 2)))
            self.list3[i] = QComboBox()
            self.list3[i].setEditable(True)
            self.list3[i].addItems(self.cond)
            self.list3[i].setValidator(comboValidator(self.list3[i]))
            self.list3[i].setCompleter(QCompleter(self.cond))
            grid.addWidget(self.list3[i], i + 1, 3)

        self.show()

    def apply(self):
        for i in range(self.nb):
            self.bt_idx[i] = self.get_type_ID(self.list2[i].currentText())
            self.bc_idx[i] = self.get_cond_ID(self.list3[i].currentText())
        print(self.bt_idx)
        print(self.bc_idx)


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
