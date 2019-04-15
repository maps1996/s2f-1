#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from fish.solver_parameter import *
from fish.spherical_harmonics import *


class setSP(QDialog):
    def __init__(self, parent=None, modal=0):
        QDialog.__init__(self, parent)
        self.setObjectName("Set_solver_parameter")
        self.setModal(modal)
        self.setWindowTitle('Set_solver_parameter')
        self.irst = 100
        self.eps = 1.0e-5
        # spherical parameters
        self.sph_pn = 1

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.lb1 = QLabel('spherical pn')
        self.lb2 = QLabel('eps')
        self.lb3 = QLabel('irst')
        self.bt1 = QPushButton('Apply')
        self.bt1.clicked.connect(self.apply)
        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.le3 = QLineEdit()

        grid.addWidget(self.lb1, 0, 0)
        grid.addWidget(self.le1, 0, 1)
        grid.addWidget(self.lb2, 1, 0)
        grid.addWidget(self.le2, 1, 1)
        grid.addWidget(self.lb3, 2, 0)
        grid.addWidget(self.le3, 2, 1)
        grid.addWidget(self.bt1, 2, 2)

        self.le1.setText(str(self.sph_pn))
        self.le2.setText(str(self.eps))
        self.le3.setText(str(self.irst))

        self.show()

    def apply(self):
        self.sph_pn = int(self.le1.text())
        self.eps = float(self.le2.text())
        self.irst = int(self.le3.text())
        sp = SolverParameter()
        sph = SphericalHarmonics(self.sph_pn)
        sp.eps = self.eps
        sp.irst = self.irst
        h5file = h5py.File('fish.h5', 'r+')
        sp.export_h5(h5file)
        sph.export_h5(h5file)
        h5file.close()
        print(self.sph_pn)
        print(self.eps)
        print(self.irst)
