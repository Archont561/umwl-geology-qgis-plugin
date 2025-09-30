from umwl_geology.qgis_plugin import UMWLGeologyPlugin

def classFactory(iface):
    return UMWLGeologyPlugin(iface)