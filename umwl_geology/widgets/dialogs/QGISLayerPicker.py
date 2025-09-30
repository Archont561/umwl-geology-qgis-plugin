from typing import List

from qgis.PyQt.QtWidgets import QDialog, QMessageBox
from qgis.PyQt.QtCore import pyqtSignal

from umwl_geology.widgets.dialogs.ui_QGISLayerPickerDialog import Ui_QGISLayerPicker
from umwl_geology.constants import PolishAdministrativeLayers, AdministrativeLayer


class QGISLayerPickerDialog(QDialog):

    layers_picked = pyqtSignal(PolishAdministrativeLayers, name="layers_picked")

    def __init__(self, *, parent=None):
        super().__init__(parent)
        self.ui = Ui_QGISLayerPicker()
        self.ui.setupUi(self)

        self._polish_administrative_layers: PolishAdministrativeLayers | None = None

        self.ui.voivodeshipNameFieldComboBox.currentIndexChanged.connect(lambda: self.ui.countyTab.setEnabled(True))
        self.ui.countyNameFieldComboBox.currentIndexChanged.connect(lambda: self.ui.communeTab.setEnabled(True))
        self.ui.communeNameFieldComboBox.currentIndexChanged.connect(lambda: self.ui.regionTab.setEnabled(True))
        self.ui.regionNameFieldComboBox.currentIndexChanged.connect(lambda: self.ui.parcelTab.setEnabled(True))
        self.ui.parcelNameFieldComboBox.currentIndexChanged.connect(lambda: self.ui.confirmButton.setEnabled(True))
        self.ui.confirmButton.clicked.connect(self._perform_check)

    def _perform_check(self):
        polish_administrative_layers = PolishAdministrativeLayers()
        flag = True

        layers: List[str]  = ['voivodeship','county','commune','region','parcel']

        for layer_name in layers:
            layer = getattr(self.ui, f'{layer_name}MapLayerComboBox').currentLayer()
            teryt_field = getattr(self.ui, f'{layer_name}TerytFieldComboBox').currentField()
            name_field = getattr(self.ui, f'{layer_name}NameFieldComboBox').currentField()

            flag = all((layer, teryt_field, name_field))

            if not flag:
                break

            setattr(polish_administrative_layers, layer_name.title(), AdministrativeLayer(
                vector_layer=layer,
                teryt_field=teryt_field,
                name_field=name_field,
            ))

        if flag:
            self._polish_administrative_layers = polish_administrative_layers
            self.layers_picked.emit(polish_administrative_layers)
        else:
            QMessageBox.critical(self, "Error", "Please select all required layers and fields.")


    # ----------- API ------------

    def get_polish_administrative_layers(self):
        return self._polish_administrative_layers


def main():
    dialog = QGISLayerPickerDialog()
    dialog.exec_()


if __name__ == '__main__':
    from umwl_geology.utils import run_in_project
    run_in_project(main)