import logging
from five import grok
from zope.component.interfaces import IObjectEvent
from zope.component.interfaces import ObjectEvent


class ITuneInTuneSetModified(IObjectEvent):
    """This event should be fired when a tune inside a tuneset is modified
    """



class TuneInTuneSetModified(ObjectEvent):
    grok.implements(ITuneInTuneSetModified)

"""
    def __init__(self, object):
        self.object = object
"""
