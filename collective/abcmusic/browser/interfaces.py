from zope import interface
from zope.viewlet.interfaces import IViewletManager


class IABCMusicLayer(interface.Interface):
    """Marker interface that defines a Zope 3 browser layer."""

class IABCMusicViewletManager(IViewletManager):
    """Marker interface for the ABCMusic viewlet manager"""
