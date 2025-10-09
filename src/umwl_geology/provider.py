from .algorithms import ExplodeTableAlgorithm
from .utils.processing_provider import ProcessingProvider


class Provider(ProcessingProvider):
    ALGORITHMS = [
        ExplodeTableAlgorithm(),
    ]
    ID = "umwl_geology"
    NAME = "UMWL Geology"
