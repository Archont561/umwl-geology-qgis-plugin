from src.ui.ui_ULDKParcelsDownloaderDialog import Ui_Dialog
from qgis.PyQt.QtWidgets import QDialog


class ULDKParcelsDownloaderDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.editingToolbar = None

    def showEditingToolbar(self):
        raise NotImplementedError

    def downloadULDKParcel(self):
        raise NotImplementedError