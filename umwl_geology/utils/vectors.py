from qgis.core import QgsFields, QgsField, QgsFeature, QVariant
from typing import List, Dict, Optional, Union


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

    get_feature_attribute = (
        lambda fields:
            lambda name: feature[(idx := fields.indexFromName(name))] if idx != -1 else None
    )(feature.fields())
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
