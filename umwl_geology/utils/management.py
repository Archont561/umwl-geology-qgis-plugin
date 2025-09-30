from typing import List, Dict, Union
from contextlib import contextmanager

from qgis.core import (
    QgsProject,
    QgsLayerTreeGroup,
    QgsMapLayer,
    QgsLayerTreeLayer,
    QgsVectorLayer,
    QgsCoordinateTransform,
    QgsFields,
    QgsField,
    QgsFeature,
)

from umwl_geology.exceptions import QGISEditingError


def copy_layer_schema(
    fields: QgsFields,
    field_names_to_remove: List[str] = None,
    fields_to_add: List[QgsField] = None
) -> QgsFields:
    """
    Create a new QgsFields schema based on the input, with optional field removal and addition.

    :param fields: Input QgsFields (from a layer or source)
    :param field_names_to_remove: List of field names to remove
    :param fields_to_add: List of QgsField objects to add
    :return: New QgsFields with modifications applied
    """
    field_names_to_remove = field_names_to_remove or []
    fields_to_add = fields_to_add or []

    new_fields = QgsFields()

    # Add all fields except those marked for removal
    for i in range(fields.count()):
        field = fields[i]
        if field.name() not in field_names_to_remove:
            new_fields.append(field)

    # Add new fields
    for field in fields_to_add:
        new_fields.append(field)

    return new_fields


def get_feature_attribute(feature: QgsFeature, field_name: str):
    idx = feature.fields().indexFromName(field_name)
    if idx != -1:
        return feature[idx]
    else:
        return None


def create_new_feature(
    feature: QgsFeature,
    schema: QgsFields,
    attribute_values: Dict[str, Union[None, int, float, str, bool]] = None
) -> QgsFeature:
    """
    Create a new QgsFeature based on a target schema (QgsFields).
    Only fields present in the schema are included. Values are taken from the original feature
    if the field exists in the source; otherwise, set to NULL or overridden via attribute_values.

    :param feature: Source feature to copy data from
    :param schema: Target QgsFields schema (defines output fields)
    :param attribute_values: Optional dict to override or set values for fields in the schema
    :return: QgsFeature compatible with the target schema
    """
    new_feat = QgsFeature(schema)
    new_feat.setGeometry(feature.geometry())
    attribute_values = attribute_values or {}
    attrs = []

    for i in range(schema.count()):
        field = schema[i]
        field_name = field.name()

        value = get_feature_attribute(feature, field_name)

        # Override with provided value
        if field_name in attribute_values:
            value = attribute_values[field_name]

        attrs.append(value)

    new_feat.setAttributes(attrs)
    return new_feat


def get_or_create_layer_group(group_name: str) -> QgsLayerTreeGroup:
    root = QgsProject.instance().layerTreeRoot()
    group = root.findGroup(group_name)
    if not group:
        group = root.addGroup(group_name)
    return group


def add_layer_to_group(layer: QgsMapLayer, group: QgsLayerTreeGroup) -> QgsLayerTreeLayer | None:
    QgsProject.instance().addMapLayer(layer, False)
    return group.addLayer(layer)


def update_layer(source: QgsVectorLayer, target: QgsVectorLayer) -> int:
    transformer = QgsCoordinateTransform(
        source.crs(),
        target.crs(),
        QgsProject.instance(),
    )

    with edit_layer(target) as layer:
        features_to_append = []
        for feature in source.getFeatures():
            new_feature = QgsFeature(feature)
            new_feature.geometry().transform(transformer)
            features_to_append.append(new_feature)
        layer.addFeatures(features_to_append)

    return len(features_to_append)


@contextmanager
def edit_layer(layer: QgsVectorLayer):
    """
    Custom context manager to safely edit a QgsVectorLayer.
    Ensures changes are committed on success, rolled back on error.
    """
    if not layer.isEditable():
        layer.startEditing()

    try:
        yield layer
        if layer.isEditable():
            success = layer.commitChanges()
            if not success:
                layer.rollBack()
                raise QGISEditingError(layer)
    finally:
        if layer.isEditable():
            layer.rollBack()
