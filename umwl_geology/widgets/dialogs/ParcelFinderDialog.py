from __future__ import annotations
from typing import List

from qgis.PyQt.QtWidgets import QDialog, QComboBox
from qgis.PyQt.QtCore import pyqtSignal

from umwl_geology.utils import iface
from umwl_geology.constants import PolishAdministrativeLayers, AdministrativeLayer
from umwl_geology.widgets.dialogs.ui_ParcelFinderDialog import Ui_ParcelFinderDialog
from umwl_geology.widgets.custom.QLinkedCombobox import QLinkedCombobox, ComboboxItem, ComboboxItemLoader


class ParcelFinderDialog(QDialog):

    layers_loaded = pyqtSignal(name="layers_loaded")

    def __init__(self, *, parent=None):
        super().__init__(parent)
        self.ui = Ui_ParcelFinderDialog()
        self.ui.setupUi(self)
        self._current_parcel_teryt: str | None = None
        self._polish_administrative_layers: PolishAdministrativeLayers | None = None

        self.ui.voivodeshipComboBox.set_child(self.ui.countyComboBox)
        self.ui.countyComboBox.set_child(self.ui.communeComboBox)
        self.ui.communeComboBox.set_child(self.ui.regionComboBox)
        self.ui.regionComboBox.set_child(self.ui.parcelComboBox)

        self.ui.voivodeshipComboBox.define_itemset_loader(self._itemset_loader_factory(self._polish_administrative_layers.Voivodeship))
        self.ui.countyComboBox.define_itemset_loader(self._itemset_loader_factory(self._polish_administrative_layers.County))
        self.ui.communeComboBox.define_itemset_loader(self._itemset_loader_factory(self._polish_administrative_layers.Commune))
        self.ui.regionComboBox.define_itemset_loader(self._itemset_loader_factory(self._polish_administrative_layers.Region))

        self.ui.parcelComboBox.currentIndexChanged.connect(self._enable_zoom_button)
        self.ui.parcelZoomButton.clicked.connect(self._search_parcel)
        self.layers_loaded.connect(self._on_layers_loaded)

    @staticmethod
    def _itemset_loader_factory(layer: AdministrativeLayer) -> ComboboxItemLoader:
        def itemset_loader(dataset: ComboboxItem) -> List[ComboboxItem]:
            _, teryt = dataset
            layer.select_by_teryt(teryt)
            combobox_items = []
            for feature in layer.vector_layer.getSelectedFeatures():
                teryt = feature.attribute(layer.teryt_field)
                name = feature.attribute(layer.teryt_field)
                combobox_items.append((f'{teryt}| {name}', teryt))
            return combobox_items

        return itemset_loader

    def _on_layers_loaded(self):
        voivodeship = self._polish_administrative_layers.Voivodeship
        self.ui.voivodeshipComboBox.setEnabled(True)
        for feature in voivodeship.vector_layer.getFeatures():
            teryt = feature.attribute(voivodeship.teryt_field)
            name = feature.attribute(voivodeship.teryt_field)
            self.ui.voivodeshipComboBox.addItem(f'{teryt}| {name}', teryt)

    def _on_parcel_combobox_index_change(self):
        self._current_parcel_teryt = self.ui.parcelComboBox.currentData()
        self._enable_zoom_button()

    def _refresh_comboboxes(self, combobox: QLinkedCombobox | QComboBox):
        self._disable_zoom_button()
        current_combobox = combobox
        while current_combobox:
            current_combobox.clear()
            current_combobox.setDisabled(True)
            current_combobox = getattr(current_combobox, "child_combobox", None)

    def _enable_zoom_button(self):
        if not self.ui.parcelZoomButton.isEnabled():
            self.ui.parcelZoomButton.setEnabled(True)

    def _disable_zoom_button(self):
        if self.ui.parcelZoomButton.isEnabled():
            self.ui.parcelZoomButton.setEnabled(False)

    def _search_parcel(self):
        parcel_layer = self._polish_administrative_layers.Parcel
        parcel_layer.select_by_teryt(self._current_parcel_teryt)
        iface.mapCanvas().zoomToSelected(parcel_layer.vector_layer)

    # ------------ API ---------------

    def load_admin_layers(self, polish_administrative_layers: PolishAdministrativeLayers):
        self._polish_administrative_layers = polish_administrative_layers
        self._refresh_comboboxes(self.ui.voivodeshipComboBox)
        self.layers_loaded.emit()

    def get_parcel_teryt(self):
        return self._current_parcel_teryt


def main():
    dialog = ParcelFinderDialog()
    dialog.exec_()


if __name__ == '__main__':
    from umwl_geology.utils import run_in_project
    run_in_project(main)