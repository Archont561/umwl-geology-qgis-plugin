from src.ui.ui_CSVLoaderDialog import Ui_CSVLoaderDialog
from qgis.PyQt.QtWidgets import QDialog


class CSVLoaderDialog(QDialog, Ui_CSVLoaderDialog):

    def __init__(self, parent=None, *args, **kwargs):
        super(Ui_CSVLoaderDialog, self).__init__(parent, *args, **kwargs)

    def loadCsv(self):
        raise NotImplementedError