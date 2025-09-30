from __future__ import annotations
from typing import Optional
from dataclasses import dataclass, field
import re

from qgis.core import QgsVectorLayer


class PolishAdministrativeLayers:
    Voivodeship: AdministrativeLayer
    County: AdministrativeLayer
    Commune: AdministrativeLayer
    Region: AdministrativeLayer
    Parcel: AdministrativeLayer


@dataclass(order=True)
class AdministrativeLayer:
    vector_layer: QgsVectorLayer = field(compare=False)
    teryt_field: str = field(compare=False)
    name_field: str = field(compare=False)
    teryt_regex: Optional[str] = field(compare=False, default=None)

    @classmethod
    def validate_teryt(cls, admin_layer: 'AdministrativeLayer', teryt: str) -> bool:
        """
        Validate TERYT string using optional regex.
        If teryt_regex is None, assume valid (or add custom logic).
        """
        if not isinstance(teryt, str):
            return False
        if admin_layer.teryt_regex is None:
            # No regex provided → assume valid? Or check non-empty?
            return len(teryt.strip()) > 0  # minimal sanity check
        try:
            pattern = re.compile(admin_layer.teryt_regex)
            return bool(pattern.fullmatch(teryt))
        except re.error:
            # In case regex is malformed
            return False

    def select_by_teryt(self, teryt: str):
        if not self.__class__.validate_teryt(self, teryt):
            raise ValueError(f"'{teryt}' is not a valid teryt!")
        self.vector_layer.selectByExpression(f"'{self.teryt_field}' = '{teryt}'")