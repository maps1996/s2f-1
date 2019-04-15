import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


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
