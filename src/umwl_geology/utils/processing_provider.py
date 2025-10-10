from qgis.core import QgsProcessingProvider
from PyQt5.QtGui import QIcon


class ProcessingProvider(QgsProcessingProvider):
    UNIQUE_PROVIDER_CONFIGURATION = {
        "ALGORITHMS": [],
        "ID": None,
        "NAME": None,
        "ICON": None,
    }

    def loadAlgorithms(self):
        for algorithm in self.UNIQUE_PROVIDER_CONFIGURATION["ALGORITHMS"]: self.addAlgorithm(algorithm)

    def id(self) -> str:
        unique_id =  self.UNIQUE_PROVIDER_CONFIGURATION.get("ID", None)
        if unique_id:
            return unique_id

        unique_id = self.UNIQUE_PROVIDER_CONFIGURATION.get("NAME", None)
        if unique_id:
            return unique_id.lower().replace(' ', '_')

        return "unknown_provider"

    def name(self) -> str:
        return self.tr(self.UNIQUE_PROVIDER_CONFIGURATION.get("NAME", "Unknown Provider"))

    def icon(self) -> QIcon:
        return self.UNIQUE_PROVIDER_CONFIGURATION["ICON"] or QgsProcessingProvider.icon(self)
