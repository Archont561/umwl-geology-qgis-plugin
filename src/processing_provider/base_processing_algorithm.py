from qgis.core import QgsProcessingAlgorithm

from qgis.PyQt.QtCore import QCoreApplication
from abc import ABC, abstractmethod


class BaseProcessingAlgorithmCoreCode(ABC):

    def __init__(self,
        should_cancel: callable = None,
        set_progress: callable = None,
        log: callable = None
    ):
        self.should_cancel = should_cancel or (lambda: False)
        self.set_progress = set_progress or self._print_progress
        self.log = log or print

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def _print_progress(progress: float):
        """ Replacement for the GUI progress bar """

        print(f'Progress: {progress:%}')


class BaseProcessingAlgorithm(QgsProcessingAlgorithm):

    NAME = None
    GROUP_NAME = None

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def __init__(self, *args, **kwargs):
        if self.NAME is None:
            raise ValueError(f"No name set for {self.__class__.name}!")
        if self.GROUP_NAME is None:
            raise ValueError(f"No group name set for {self.__class__.name}!")
        super().__init__(*args, **kwargs)

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def name(self):
        return self.NAME.lower().replace(' ', '_')

    def displayName(self):
        return self.tr(self.NAME)

    def group(self):
        return self.tr(self.GROUP_NAME)

    def groupId(self):
        return self.GROUP_NAME.lower().replace(' ', '_')

    def createInstance(self):
        return self.__class__()