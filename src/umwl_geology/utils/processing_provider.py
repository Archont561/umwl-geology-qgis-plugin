from typing import Optional, List

from qgis.core import QgsProcessingProvider, QgsProcessingAlgorithm
from PyQt5.QtGui import QIcon


class ProcessingProvider(QgsProcessingProvider):
    ALGORITHMS: List[QgsProcessingAlgorithm] = []
    ID: Optional[str] = None
    NAME: Optional[str] = None
    ICON: Optional[QIcon] = None

    def loadAlgorithms(self):
        for algorithm in self.__class__.ALGORITHMS: self.addAlgorithm(algorithm)

    def id(self) -> str:
        return self.__class__.__name__.ID or self.__class__.NAME.lower().replace(' ', '_')

    def name(self) -> str:
        return self.tr(self.__class__.NAME)

    def icon(self) -> QIcon:
        return self.__class__.ICON or QgsProcessingProvider.icon(self)
