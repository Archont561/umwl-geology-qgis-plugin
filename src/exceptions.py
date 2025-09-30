from qgis.core import QgsVectorLayer


class QGISPluginError(Exception):
    ...

class QGISEditingError(Exception):
    """
    Custom exception for vector layer editing failures.
    Stores the layer and formatted commit errors.
    """
    def __init__(self, layer: QgsVectorLayer):
        self.layer = layer
        message = self.format_message()
        super().__init__(message)

    def format_message(self) -> str:
        """Format a user-friendly error message."""
        header = f"Editing failed for layer '{self.layer.name()}'"
        errors = self.layer.commitErrors()
        details = "\n  ".join(errors) if errors else "Unknown error"
        return f"{header}:\n  {details}"

    def __str__(self):
        return self.format_message()

    def log_error(self):
        """Print or log detailed error."""
        print(f"❌ Editing Error on Layer: {self.layer.name()}")
        print(f"   Source: {self.layer.source()}")
        for err in self.layer.commitErrors():
            print(f"   • {err}")


class QGISProjectNotFoundError(QGISPluginError):
    ...

class QGISMapLayerNotFoundError(QGISPluginError):
    ...