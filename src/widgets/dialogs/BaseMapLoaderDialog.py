from src.ui.ui_BaseMapLoaderDialog import Ui_Dialog
from PyQt5.QtWidgets import QDialog


class BaseMapLoaderDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def loadBasemap(self):
        raise NotImplementedError

    def removeBasemap(self):
        raise NotImplementedError