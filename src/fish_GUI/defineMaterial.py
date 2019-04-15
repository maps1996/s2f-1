#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from fish_GUI.combobox import *

import fish_GUI.make_transx_input as make_input


_nuclide_list = ['al27 ', 'c12  ', 'cr52 ', 'fe54 ', 'h2   ', 'li7  ', 'mo95 ', 'na23 ',
                 'ni64 ', 'si28 ', 'ti46 ', 'w182 ', 'au197', 'canat', 'cr53 ', 'fe56 ',
                 'h3   ', 'mgnat', 'mo96 ', 'nb93 ', 'o16  ', 'si29 ', 'ti47 ', 'w183 ',
                 'b10  ', 'cl35 ', 'cr54 ', 'fe57 ', 'he3  ', 'mn55 ', 'mo97 ', 'ni58 ',
                 'p31  ', 'si30 ', 'ti48 ', 'w184 ', 'b11  ', 'cl37 ', 'cu63 ', 'fe58 ',
                 'he4  ', 'mo100', 'mo98 ', 'ni60 ', 'pb206', 'snat ', 'ti49 ', 'w186 ',
                 'be9  ', 'co59 ', 'cu65 ', 'ganat', 'knat ', 'mo92 ', 'n14  ', 'ni61 ', 'pb207',
                 'snnat', 'ti50 ', 'zrnat', 'bi209', 'cr50 ', 'f19  ', 'h1   ', 'li6  ',
                 'mo94 ', 'n15  ', 'ni62 ', 'pb208', 'ta181', 'vnat ']


class defineMaterial(QDialog):
    def __init__(self, parent=None, modal=0):
        QDialog.__init__(self, parent)
        self.setObjectName("Material")
        self.setModal(modal)
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)

        btn = QPushButton('Apply')
        pts = QLabel('Particle')

        apply_btn = QPushButton('Apply')
        new_btn = QPushButton('New')
        del_btn = QPushButton('Delete')
        applymat_btn = QPushButton('Apply')
        applyexs_btn = QPushButton('Apply')
        delmat_btn = QPushButton('Delete')
        delexs_btn = QPushButton('Delete')
        path_btn = QPushButton('data path')

        lb1 = QLabel('Nuclide')
        lb2 = QLabel('Density')
        lb3 = QLabel('Material Name')
        lb4 = QLabel('Legendre order')
        lb5 = QLabel('Extra xs')

        btn.clicked.connect(self.apply)
        applymat_btn.clicked.connect(self.apply1)
        applyexs_btn.clicked.connect(self.apply2)
        apply_btn.clicked.connect(self.make)

        del_btn.clicked.connect(self.delete)
        delmat_btn.clicked.connect(self.delete1)
        delexs_btn.clicked.connect(self.delete2)
        path_btn.clicked.connect(self.setpath)

        self.MatList = []
        self.NumMat = 0
        self.MatList1 = []

        self.Exslist = []
        self.Numexs = 0

        self.MatListWidget = QListWidget()
        self.NucListWidget = QListWidget()
        self.ExsListWidget = QListWidget()

        self.MatListWidget.itemClicked.connect(self.showMatComponent)

        self.le1 = QComboBox()
        self.le1.setEditable(True)
        self.le1.addItems(_nuclide_list)
        self.le1.setValidator(comboValidator(self.le1))
        self.le1.setCompleter(QCompleter(_nuclide_list))
        self.le2 = QLineEdit()
        self.le2.setValidator(QDoubleValidator())

        self.le3 = QLineEdit()
        self.le4 = QLineEdit()
        self.le5 = QLineEdit()
        self.le0 = QComboBox()
        self.le0.addItem("neutron")
        self.le0.addItem("gamma")
        self.le0.addItem("neutron and gamma")

        layout.addWidget(pts, 0, 1, 1, 1)
        layout.addWidget(self.le0, 0, 2, 1, 2)
        layout.addWidget(path_btn, 0, 4, 1, 1)

        layout.addWidget(self.MatListWidget, 0, 0, 3, 1)
        layout.addWidget(self.NucListWidget, 2, 1, 1, 6)
        layout.addWidget(self.ExsListWidget, 3, 0, 3, 1)

        layout.addWidget(lb1, 3, 1)
        layout.addWidget(self.le1, 3, 2)
        layout.addWidget(lb2, 3, 3)
        layout.addWidget(self.le2, 3, 4)
        layout.addWidget(btn, 3, 5)
        layout.addWidget(del_btn, 3, 6)

        layout.addWidget(lb3, 1, 1, 1, 1)
        layout.addWidget(self.le3, 1, 2, 1, 3)
        layout.addWidget(applymat_btn, 1, 5)
        layout.addWidget(delmat_btn, 1, 6)

        layout.addWidget(lb4, 0, 5)
        layout.addWidget(self.le4, 0, 6)

        layout.addWidget(lb5, 4, 1)
        layout.addWidget(self.le5, 4, 2, 1, 3)
        layout.addWidget(applyexs_btn, 4, 5)
        layout.addWidget(delexs_btn, 4, 6)

        layout.addWidget(new_btn, 5, 1, 1, 1)
        layout.addWidget(apply_btn, 5, 5, 1, 1)

        self.setWindowTitle('Material')
        self.show()

    def setpath(self):
        self.datapath = QFileDialog.getExistingDirectory(self,
                                                         "选取文件夹",
                                                         "./")
        self.datapath = self.datapath + "/"

    def showMatComponent(self, item):
        row = self.MatListWidget.currentRow()
        self.NucListWidget.clear()
        for i in range(self.MatList[row].NumNuclide):
            _item = QListWidgetItem(
                str(self.MatList[row].Nuclide[i]) + '   ' + str(self.MatList[row].Density[i]), self.NucListWidget)

    def apply(self):
        row = self.MatListWidget.currentRow()
        t = 0
        if self.NucListWidget.count() == 0:
            self.MatList[row].addNuclide(
                str(self.le1.currentText()), str(self.le2.text()))
            self.NucListWidget.clear()
            for i in range(self.MatList[row].NumNuclide):
                _item = QListWidgetItem(
                    str(self.MatList[row].Nuclide[i]) + '   ' + str(self.MatList[row].Density[i]), self.NucListWidget)
        else:
            for i in range(self.MatList[row].NumNuclide):
                if self.le1.currentText() == self.MatList[row].Nuclide[i]:
                    t = 1
            if t == 1:
                reply = QMessageBox.critical(
                    self, "error", "The nuclides component already exist.", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            else:
                self.MatList[row].addNuclide(
                    str(self.le1.currentText()), str(self.le2.text()))
                self.NucListWidget.clear()
                for i in range(self.MatList[row].NumNuclide):
                    _item = QListWidgetItem(
                        str(self.MatList[row].Nuclide[i]) + '   ' + str(self.MatList[row].Density[i]), self.NucListWidget)

    def apply1(self):
        NewMat = Mat(str(self.le3.text()))
        t = 0
        if self.MatListWidget.count() == 0:
            self.MatList.append(NewMat)
            self.MatList1.append(NewMat.Name)
            self.NumMat = self.NumMat + 1
            _item = QListWidgetItem(NewMat.Name, self.MatListWidget)
        else:
            for i in range(self.NumMat):
                if NewMat.Name == self.MatList1[i]:
                    t = 1
            if t == 1:
                reply = QMessageBox.critical(
                    self, "error", "The material has been created", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            else:
                self.MatList.append(NewMat)
                self.MatList1.append(NewMat.Name)
                self.NumMat = self.NumMat + 1
                _item = QListWidgetItem(NewMat.Name, self.MatListWidget)

    def apply2(self):
        Newexs = str(self.le5.text())
        t = 0
        if self.ExsListWidget.count() == 0:
            self.Exslist.append(Newexs)
            self.Numexs = self.Numexs + 1
            _item = QListWidgetItem(Newexs, self.ExsListWidget)
        else:
            for exs in self.Exslist:
                if Newexs == exs:
                    t = 1
            if t == 1:
                reply = QMessageBox.critical(
                    self, "error", "The extra cross section has been created", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            else:
                self.Exslist.append(Newexs)
                self.Numexs = self.Numexs + 1
                _item = QListWidgetItem(Newexs, self.ExsListWidget)

    def delete(self):
        row = self.MatListWidget.currentRow()
        row1 = self.NucListWidget.currentRow()
        del self.MatList[row].Nuclide[row1]
        self.MatList[row].NumNuclide -= 1
        self.NucListWidget.takeItem(self.NucListWidget.currentRow())

    def delete1(self):
        row = self.MatListWidget.currentRow()
        self.MatList[row].Nuclide = []
        del self.MatList[row]
        del self.MatList1[row]
        self.NumMat -= 1
        self.MatListWidget.takeItem(self.MatListWidget.currentRow())
        self.NucListWidget.clear()

    def delete2(self):
        row = self.ExsListWidget.currentRow()
        del self.Exslist[row]
        self.Numexs -= 1
        self.ExsListWidget.takeItem(self.ExsListWidget.currentRow())
    # use make_transx_input

    def make(self):
        if self.le0.currentText() == "neutron":
            ng = True
            gg = False
        elif self.le0.currentText() == "gamma":
            ng = False
            gg = True
        else:
            ng = True
            gg = True
        NREG = self.MatListWidget.count()
        NMIX = self.MatListWidget.count()
        NL = int(self.le4.text())
        NMIXS = 0
        c1 = make_input.card1()
        c2 = make_input.card2(ng, gg)
        list1 = []
        for i in range(NMIX):
            list1.append(self.MatListWidget.item(i).text())
        c4, names = make_input.card4(list1)
        c5 = make_input.card5(NMIX)
        c6 = make_input.card6()
        list2 = []
        c7 = ""
        for i in range(NMIX):
            for j in range(self.MatList[i].NumNuclide):
                list2.append(
                    str(self.MatList[i].Nuclide[j]) + '   ' + str(self.MatList[i].Density[j]))
                NMIXS = NMIXS + 1
                c7 += " {}    {}    {}/\n".format(i + 1, i + 1,
                                                  str(self.MatList[i].Nuclide[j]) + '   ' + str(self.MatList[i].Density[j]))
        c3 = make_input.card3(self.datapath, ng, gg,
                              NMIX, NMIXS, NL, self.Numexs)
        c8 = make_input.card8(self.Exslist)
        c9 = make_input.card9(self.Exslist)

        total = c1 + c2 + c3 + c4 + c5 + c7 + c8 + c9 + 'stop'
        input_file = open('transx.inp', 'w+')
        input_file.write(total)
        input_file.close()
        print(input_file.closed)
        os.system('transx')


class Mat():
    """docstring for MatList."""

    def __init__(self, name):
        self.Name = name
        self.NumNuclide = 0
        self.Nuclide = []
        self.Density = []

    def addNuclide(self, name, density):
        self.NumNuclide = self.NumNuclide + 1
        self.Nuclide.append(name)
        self.Density.append(density)
