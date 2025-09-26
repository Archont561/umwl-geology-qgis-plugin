from src.ui.ui_MineralDepositAnalyzerDialog import Ui_Dialog
from qgis.PyQt.QtWidgets import QDialog

class MineralDepositAnalyzerDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def checkDeposit(self):
        raise NotImplementedError
