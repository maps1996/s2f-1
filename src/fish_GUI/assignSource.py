#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from fish.source import *


class assignSrc(QDialog):
    def __init__(self, parent=None, modal=0):
        QDialog.__init__(self, parent)
        self.setObjectName('Source')
        self.setModal(modal)
        self.setWindowTitle('Source')

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.list1 = []
        self.list2 = []
        self.NumSrc = 0
        self.SrcList = []
        self.SrcList1 = []

        self.lb1 = QLabel('Source spectrum')
        self.lb2 = QLabel('Source name')
        self.lb3 = QLabel('Source list')
        self.le1 = QTextEdit()
        self.le2 = QLineEdit()
        self.SrcListWidget = QListWidget()
        self.bt1 = QPushButton('Apply')
        self.bt2 = QPushButton('Apply')
        self.bt3 = QPushButton('Delete')
        self.bt4 = QPushButton('Export')

        grid.addWidget(self.lb1, 0, 0)
        grid.addWidget(self.le1, 1, 0, 5, 2)
        grid.addWidget(self.bt1, 5, 2)
        grid.addWidget(self.lb2, 2, 2)
        grid.addWidget(self.le2, 2, 3)
        grid.addWidget(self.bt2, 2, 4)
        grid.addWidget(self.bt3, 3, 4)
        grid.addWidget(self.bt4, 5, 4)
        grid.addWidget(self.lb3, 0, 3)
        grid.addWidget(self.SrcListWidget, 1, 3, 1, 1)

        self.bt1.clicked.connect(self.apply)
        self.bt2.clicked.connect(self.apply1)
        self.bt3.clicked.connect(self.delete)
        self.bt4.clicked.connect(self.export)
        self.SrcListWidget.itemClicked.connect(self.showSrcComponent)

        self.show()

    def showSrcComponent(self, item):
        row = self.SrcListWidget.currentRow()
        self.le1.clear()
        dis = ''
        for i in range(len(self.SrcList[row].list)):
            if i == 0:
                dis = dis + str(self.SrcList[row].list[i])
            else:
                dis = dis + ' ' + str(self.SrcList[row].list[i])
        self.le1.setPlainText(dis)

    def apply(self):
        row = self.SrcListWidget.currentRow()
        self.list1 = self.le1.toPlainText().splitlines()
        m = ''
        for i in range(len(self.list1)):
            if i == 0:
                m = m + self.list1[i]
            else:
                m = m + ' ' + self.list1[i]
        list1 = []
        list1 = m.split()
        for f in list1:
            self.list2.append(float(f))
        self.SrcList[row].addSource(self.list2)
        self.list2 = []

    def export(self):
        h5file = h5py.File('fish.h5', 'r+')
        pref='source'
        if pref in h5file.keys():
            h5file.__delitem__(pref)
        h5file['/source/ns'] = self.NumSrc
        for i in range(self.NumSrc):
            h5_src = Source_h5(
                self.SrcList1[i], self.SrcList[i].list)
            h5_src.export_h5(h5file)
        h5file.close()

    def apply1(self):
        self.le1.clear()
        NewSrc = Source(str(self.le2.text()))
        t = 0
        if self.SrcListWidget.count() == 0:
            self.SrcList.append(NewSrc)
            self.SrcList1.append(NewSrc.Name)
            self.NumSrc = self.NumSrc + 1
            _item = QListWidgetItem(NewSrc.Name, self.SrcListWidget)
        else:
            for i in range(self.NumSrc):
                if NewSrc.Name == self.SrcList1[i]:
                    t = 1
            if t == 1:
                reply = QMessageBox.critical(
                    self, "error", "The source has been created", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            else:
                self.SrcList.append(NewSrc)
                self.SrcList1.append(NewSrc.Name)
                self.NumSrc = self.NumSrc + 1
                _item = QListWidgetItem(NewSrc.Name, self.SrcListWidget)
        print(self.SrcList1)

    def delete(self):
        row = self.SrcListWidget.currentRow()
        self.SrcList[row].list = []
        del self.SrcList[row]
        del self.SrcList1[row]
        self.NumSrc -= 1
        self.SrcListWidget.takeItem(self.SrcListWidget.currentRow())
        self.le1.clear()


class Source():

    def __init__(self, name):
        self.Name = name

    def addSource(self, src_list):
        self.list = src_list
