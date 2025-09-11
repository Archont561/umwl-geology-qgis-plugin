from umwl_geology.UMWLGeologyPlugin import UMWLGeologyPlugin

def classFactory(iface):
    return UMWLGeologyPlugin(iface)