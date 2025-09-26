from src.ui.ui_ULDKParcelFinderDialog import Ui_uldkParcelFinderDialog
from qgis.PyQt.QtWidgets import QDialog, QComboBox


class ULDKParcelFinderDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_uldkParcelFinderDialog()
        self.ui.setupUi(self)

    def populateCombobox(self, value: str, combobox: QComboBox):
        raise NotImplementedError

    def searchParcel(self, parcelID: str):
        raise NotImplementedError