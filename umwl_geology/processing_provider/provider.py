from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from umwl_geology.processing_provider.explode_table import ExplodeTableAlgorithm

class Provider(QgsProcessingProvider):

    def loadAlgorithms(self):
        self.addAlgorithm(ExplodeTableAlgorithm())

    def id(self) -> str:
        return 'umwl_geology'

    def name(self) -> str:
        return self.tr('UMWL Geology')

    def icon(self) -> QIcon:
        return QgsProcessingProvider.icon(self)