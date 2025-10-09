from typing import Optional

from qgis.core import QgsProcessingProvider
from PyQt5.QtGui import QIcon

from .algorithms import ExplodeTableAlgorithm
from .utils.algorithms import BaseProcessingAlgorithm


class Provider(QgsProcessingProvider):

    def __init__(self):
        super().__init__()
        self.algorithms = [
            ExplodeTableAlgorithm()
        ]

    def loadAlgorithms(self):
        for algorithm in self.algorithms: self.addAlgorithm(algorithm)

    def id(self) -> str:
        return 'umwl_geology'

    def name(self) -> str:
        return self.tr('UMWL Geology')

    def icon(self) -> QIcon:
        return QgsProcessingProvider.icon(self)

    def getAlgorithmByName(self, name: str) -> Optional[BaseProcessingAlgorithm]:
        for algorithm in self.algorithms:
            if algorithm.name() == name:
                return algorithm
        return None