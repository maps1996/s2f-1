
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5 import QtCore
import sys
from qtsalome import *


class FishWindowHandler():
    """Main class of FISH. Handles all calls and creates and stores
    windows. References to the windows have to be kept in memory otherwise
    they will not be shown properly."""

    def __init__(self):
        """Constructor"""
        # public fields
        self.meshDirectory = ''
        self.gsWindow = None
        self.psWindow = None

    def about(self):
        """About information window."""
        title = "FISH interface for SALOME"
        msg = "Interface that allows setup of an FISH input with the help of the Salome-paltform.\n"
        msg1 = "by Fang chao, Miao Jianxin 2018."
        QMessageBox.about(None, title, msg + msg1)

    def hello(self):
        QMessageBox.information(self, 'Information', 'Hello ', self.le.text())
