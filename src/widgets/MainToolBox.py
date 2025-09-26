from ..ui.ui_MainToolBox import Ui_pluginMainToolbar
from qgis.PyQt.QtWidgets import QDialog

from .dialogs import (
    CSVLoaderDialog,
    MineralDepositAnalyzerDialog,
    BaseMapLoaderDialog,
    ULDKParcelFinderDialog,
    ULDKParcelsDownloaderDialog,
)

from dataclasses import dataclass


class MainToolBox(QDialog):

    @dataclass
    class ActionDialogs:
        csvLoaderDialog: CSVLoaderDialog
        mineralDepositAnalyzerDialog: MineralDepositAnalyzerDialog
        baseMapLoaderDialog: BaseMapLoaderDialog
        uldkParcelFinderDialog: ULDKParcelFinderDialog
        uldkParcelsDownloaderDialog: ULDKParcelsDownloaderDialog

    def __init__(self, parent=None):
        super(MainToolBox, self).__init__(parent)
        self.ui = Ui_pluginMainToolbar()
        self.ui.setupUi(self)

        self.actionDialogs: MainToolBox.ActionDialogs = MainToolBox.ActionDialogs(
            csvLoaderDialog = CSVLoaderDialog(parent=self),
            mineralDepositAnalyzerDialog = MineralDepositAnalyzerDialog(parent=self),
            baseMapLoaderDialog = BaseMapLoaderDialog(parent=self),
            uldkParcelFinderDialog = ULDKParcelFinderDialog(parent=self),
            uldkParcelsDownloaderDialog = ULDKParcelsDownloaderDialog(parent=self),
        )

        # SIGNALS
        for signal, action in (
            (self.csvLoaderButton, self.loadCSV),
            (self.mineralDepositCheckerButton, self.analyzeMineralDeposit),
            (self.basemapToggleButton, self.loadBasemap),
            (self.uldkParcelDownloaderButton, self.downloadULDKParcels),
            (self.parcelFinderButton, self.findParcel),
        ):
            signal.connect(action)

    def show(self):
        raise NotImplementedError

    def loadCSV(self):
        raise NotImplementedError

    def analyzeMineralDeposit(self):
        raise NotImplementedError

    def loadBasemaps(self):
        raise NotImplementedError

    def downloadULDKParcels(self):
        raise NotImplementedError

    def findParcel(self):
        raise NotImplementedError