from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from .explode_table import ExplodeTableAlgorithm
from .base_processing_algorithm import BaseProcessingAlgorithm


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

    def getAlgorithmByName(self, name: str) -> BaseProcessingAlgorithm | None:
        for algorithm in self.algorithms:
            if algorithm.name() == name:
                return algorithm
        return None