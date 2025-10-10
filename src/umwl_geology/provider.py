from .algorithms import ExplodeTableAlgorithm
from .utils.processing_provider import ProcessingProvider


class Provider(ProcessingProvider):
    UNIQUE_PROVIDER_CONFIGURATION = {
        "ALGORITHMS": [
            ExplodeTableAlgorithm()
        ],
        "ID": "umwl_geology",
        "NAME": "UMWL Geology",
    }