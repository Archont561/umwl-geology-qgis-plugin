from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterString,
    QgsProcessingParameterFeatureSink,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsFeatureSink
)
from qgis.PyQt.QtCore import QVariant

from src.utils.management import copy_layer_schema, create_new_feature
from src.processing_provider.base_processing_algorithm import (
    BaseProcessingAlgorithm,
    BaseProcessingAlgorithmCoreCode
)


class ExplodeTableCode(BaseProcessingAlgorithmCoreCode):

    def __init__(self, get_progress, *args, **kwargs):
        self.get_progress = get_progress
        super().__init__(*args, **kwargs)

    def execute(self,
        features: list[QgsFeature],
        field_name_to_explode: str,
        delimiter: str,
        new_field_name: str,
        new_schema: QgsFields,
    ) -> list[QgsFeature]:
        exploded_features = []

        for i, feature in enumerate(features, start=1):
            if self.should_cancel():
                break

            value = feature[field_name_to_explode]
            parts = (part.strip() for part in str(value).split(delimiter)) if value else [None]

            for part in parts:
                new_attrs = {}
                new_attrs[new_field_name] = part

                exploded_features.append(create_new_feature(
                    feature,
                    new_schema,
                    attribute_values=new_attrs
                ))

            self.set_progress(self.get_progress(i))

        return exploded_features


class ExplodeTableAlgorithm(BaseProcessingAlgorithm):

    NAME = 'Explode Table'
    GROUP_NAME = 'Utilities'

    FIELD = 'FIELD'
    NEW_FIELD = 'NEW_FIELD'
    DELIMITER = 'DELIMITER'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                'Input layer',
                [QgsProcessing.TypeVector]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD,
                'Field to split',
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.String
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.DELIMITER,
                'Delimiter',
                defaultValue=','
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.NEW_FIELD,
                'Name for new field',
                defaultValue='exploded'
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                'Output layer'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        # Get parameters
        source = self.parameterAsSource(parameters, self.INPUT, context)
        field_name = self.parameterAsString(parameters, self.FIELD, context)
        delimiter = self.parameterAsString(parameters, self.DELIMITER, context)
        new_field_name = self.parameterAsString(parameters, self.NEW_FIELD, context)

        # Create new schema for output layer
        new_schema = copy_layer_schema(
            source.fields(),
            fields_to_remove=[field_name],
            fields_to_add=[QgsField(new_field_name, QVariant.String)]
        )

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            new_schema,
            source.wkbType(),
            source.sourceCrs()
        )

        # Execute core code in algorithm
        exploded_features = ExplodeTableCode(
            get_progress=(lambda total:
                lambda progress: progress * 100.0 / total
            )(source.featureCount()),
            set_progress=feedback.setProgress,
            log=feedback.pushInfo,
            should_cancel=feedback.isCanceled,
        ).execute(
            features=source.getFeatures(),
            field_name_to_explode=field_name,
            delimiter=delimiter,
            new_field_name=new_field_name,
            new_schema=new_schema,
        )

        if exploded_features:
            sink.addFeatures(exploded_features, QgsFeatureSink.FastInsert)

        return {self.OUTPUT: dest_id}
