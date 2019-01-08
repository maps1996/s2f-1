#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
from trans2 import *


class assignMat(QDialog):
    def __init__(self, parent=None, modal=0):
        QDialog.__init__(self, parent)
        self.setObjectName('AssignMaterial')
        self.setModal(modal)
        self.setWindowTitle('AssignMaterial')
        if len(matlist) == 0:
            init_matlist('./transx.out')
        self.Material = []
        for mat in matlist:
            self.Material.append(mat.name)
        self.Material.append('vacuum')
        self.source = []
        self.names = []

    def get_material_ID(self, mat):
        if (mat == 'm1'):
            return 1
        if (mat == 'm2'):
            return 2
        if (mat == 'm3'):
            return 3
        if (mat == 'm4'):
            return 4
        if (mat == 'm5'):
            return 5
        if (mat == 'm6'):
            return 6
        if (mat == 'vacuum'):
            return 0

    def get_source_ID(self, src):
        if (src == 's1'):
            return 1
        if (src == 's2'):
            return 2
        if (src == 's3'):
            return 3
        if (src == 'none'):
            return 0

    def setRegionNames(self, names):
        self.names = names
        self.nR = len(self.names)
        self.mat_idx = np.zeros((self.nR), dtype=np.int64)
        self.src_idx = np.zeros((self.nR), dtype=np.int64)

    def setSource(self, srclist):
        self.nsrc = len(srclist)
        for src in srclist:
            self.source.append(src)
        self.source.append('none')

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.lb1 = QLabel('Region')
        self.lb2 = QLabel('Material')
        self.lb3 = QLabel('Source')
        self.bt1 = QPushButton('Apply')
        self.bt1.clicked.connect(self.apply)

        grid.addWidget(self.lb1, 0, 0)
        grid.addWidget(self.lb2, 0, 1)
        grid.addWidget(self.lb3, 0, 2)
        grid.addWidget(self.bt1, self.nR, 3)

        le_names = locals()
        le_names1 = locals()
        self.list1 = []
        self.list2 = []
        for i in range(self.nR):
            lb = QLabel(self.names[i])
            grid.addWidget(lb, i + 1, 0)

            le_names['n' + str(i + 1)] = 'self.le' + str(i + 1)
            self.list1.append(eval('n{}'.format(i + 1)))
            self.list1[i] = QComboBox()
            self.list1[i].setEditable(True)
            print(self.Material)
            self.list1[i].addItems(self.Material)
            self.list1[i].setValidator(comboValidator(self.list1[i]))
            self.list1[i].setCompleter(QCompleter(self.Material))
            grid.addWidget(self.list1[i], i + 1, 1)

            le_names1['n' + str(self.nR + i + 1)] = 'self.le' + \
                str(self.nR + i + 1)
            self.list2.append(eval('n{}'.format(self.nR + i + 1)))
            self.list2[i] = QComboBox()
            self.list2[i].setEditable(True)
            self.list2[i].addItems(self.source)
            self.list2[i].setValidator(comboValidator(self.list2[i]))
            self.list2[i].setCompleter(QCompleter(self.source))
            grid.addWidget(self.list2[i], i + 1, 2)

        self.show()

    def apply(self):
        for i in range(self.nR):
            self.mat_idx[i] = self.get_material_ID(self.list1[i].currentText())
            self.src_idx[i] = self.get_source_ID(self.list2[i].currentText())

        print(self.mat_idx)
        print(self.src_idx)


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
