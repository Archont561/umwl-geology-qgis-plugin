from typing import Callable, List, Tuple, Optional

from PyQt5.QtWidgets import QComboBox

ComboboxItem = Tuple[str, any]
ComboboxItemLoader = Callable[[ComboboxItem], List[ComboboxItem]]


class QLinkedCombobox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.child_combobox: Optional[QComboBox] = None
        self.itemset_loader: Optional[ComboboxItemLoader] = None

    def define_itemset_loader(self, itemset_loader: ComboboxItemLoader):
        self.itemset_loader = itemset_loader

    def set_child(self, child_combo):
        try:
            self.currentIndexChanged.disconnect()
        except TypeError:
            pass
        self.itemset_loader = None
        self.child_combobox = child_combo
        self.currentIndexChanged.connect(self._handle_index_change)

    def _handle_index_change(self):
        if self.itemset_loader is None or self.child_combobox is None:
            return

        self.child_combobox.blockSignals(True)
        self.child_combobox.clear()

        # Get current item as (text, data) tuple
        current_text = self.currentText()
        current_data = self.currentData()
        current_item = (current_text, current_data if current_data is not None else current_text)

        # Load new items using the loader function
        new_items = self.itemset_loader(current_item)
        for text, user_data in new_items:
            self.child_combobox.addItem(text, user_data)

        self.child_combobox.blockSignals(False)
