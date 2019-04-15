#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from fish.mesh import *
from fish_GUI.combobox import *
mh = Mesh()


class assignMesh(QDialog):
    def __init__(self, parent=None, modal=0):
        QDialog.__init__(self, parent)
        self.setObjectName("Mesh")
        self.setModal(modal)
        self.setWindowTitle('Mesh')
        self.mesh_names = ''
        self.work_mesh = ''
        self.domain_names = []
        self.boundary_names = []

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
            'utf8').decode('utf8')
        print (">>> Assigned mesh: " + self.work_mesh)
        mh.set_work_mesh(self.work_mesh)
        nd = mh.get_dimension()
        self.domain_names = mh.get_domain_group_names()
        self.boundary_names = mh.get_boundary_group_names()
        if os.path.exists('./fish.h5'):
            h5file = h5py.File('fish.h5', 'r+')
            mh.export_h5(h5file)
            h5file.close()
        else:
            h5file = h5py.File('fish.h5', 'w')
            mh.export_h5(h5file)
            h5file.close()
