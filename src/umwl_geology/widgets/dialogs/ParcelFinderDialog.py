from __future__ import annotations
from typing import List, Optional

from qgis.gui import QgisInterface
from PyQt5.QtWidgets import QDialog, QComboBox, QMessageBox
from PyQt5.QtCore import pyqtSignal

from ...constants import PolishAdministrativeLayers, AdministrativeLayer
from ...widgets.dialogs.ui_ParcelFinderDialog import Ui_ParcelFinderDialog
from ...widgets.custom.QLinkedCombobox import ComboboxItem, ComboboxItemLoader


class ParcelFinderDialog(QDialog):

    layers_loaded = pyqtSignal(name="layers_loaded")

    def __init__(self, *, parent=None, iface: QgisInterface):
        super().__init__(parent)
        self.ui = Ui_ParcelFinderDialog()
        self.ui.setupUi(self)
        self.iface = iface
        self._current_parcel_teryt: Optional[str]= None
        self._polish_administrative_layers: Optional[PolishAdministrativeLayers] = None

        self.ui.voivodeshipComboBox.set_child(self.ui.countyComboBox)
        self.ui.countyComboBox.set_child(self.ui.communeComboBox)
        self.ui.communeComboBox.set_child(self.ui.regionComboBox)
        self.ui.regionComboBox.set_child(self.ui.parcelComboBox)

        self.ui.parcelZoomButton.clicked.connect(self._search_parcel)
        self.layers_loaded.connect(self._on_layers_loaded)

    @staticmethod
    def _itemset_loader_factory(layer: AdministrativeLayer) -> ComboboxItemLoader:
        def itemset_loader(dataset: ComboboxItem) -> List[ComboboxItem]:
            _, teryt = dataset
            expression = f'"{layer.teryt_field}" LIKE \'{teryt}%\''
            layer.vector_layer.selectByExpression(expression)
            combobox_items = []
            for feature in layer.vector_layer.getSelectedFeatures():
                teryt = feature.attribute(layer.teryt_field)
                name = feature.attribute(layer.name_field)
                combobox_items.append((f'{teryt}| {name}', teryt))
            return combobox_items

        return itemset_loader

    def _on_layers_loaded(self):
        voivodeship = self._polish_administrative_layers.Voivodeship
        self.ui.voivodeshipComboBox.setEnabled(True)
        for feature in voivodeship.vector_layer.getFeatures():
            teryt = feature.attribute(voivodeship.teryt_field)
            name = feature.attribute(voivodeship.name_field)
            self.ui.voivodeshipComboBox.addItem(f'{teryt}| {name}', teryt)

        self.ui.voivodeshipComboBox.setCurrentIndex(0)

    def _refresh_comboboxes(self, combobox: QComboBox):
        current_combobox = combobox
        while current_combobox:
            current_combobox.clear()
            current_combobox.setDisabled(True)
            current_combobox = getattr(current_combobox, "child_combobox", None)

    def _search_parcel(self):
        teryt = self.get_parcel_teryt()
        if not teryt:
            QMessageBox.critical(self, "Error", "Please select parcel teryt!")
            return

        parcel_layer = self._polish_administrative_layers.Parcel
        expression = f'"{parcel_layer.teryt_field}" = \'{teryt}\''
        parcel_layer.vector_layer.selectByExpression(expression)

        if parcel_layer.vector_layer.selectedFeatureCount() == 0:
            QMessageBox.critical(self, "Error", "No parcel found!")
            return

        self.iface.mapCanvas().zoomToSelected(parcel_layer.vector_layer)

    # ------------ API ---------------

    def load_admin_layers(self, polish_administrative_layers: PolishAdministrativeLayers):
        self._polish_administrative_layers = polish_administrative_layers
        self._refresh_comboboxes(self.ui.voivodeshipComboBox)

        self.ui.voivodeshipComboBox.define_itemset_loader(self._itemset_loader_factory(self._polish_administrative_layers.County))
        self.ui.countyComboBox.define_itemset_loader(self._itemset_loader_factory(self._polish_administrative_layers.Commune))
        self.ui.communeComboBox.define_itemset_loader(self._itemset_loader_factory(self._polish_administrative_layers.Region))
        self.ui.regionComboBox.define_itemset_loader(self._itemset_loader_factory(self._polish_administrative_layers.Parcel))

        self.layers_loaded.emit()

    def get_parcel_teryt(self):
        return self.ui.parcelComboBox.currentData()

    def are_administrative_layers_loaded(self) -> bool:
        return self._polish_administrative_layers is not None


if __name__ == '__main__':
    from ...utils.miscallenous import QGISEnvironment

    with QGISEnvironment():
        dialog = ParcelFinderDialog()
        dialog.exec_()
