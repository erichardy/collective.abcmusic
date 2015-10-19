import logging
from zope.publisher.browser import BrowserView
# from plone.namedfile.interfaces import HAVE_BLOBS
# from zope import schema
# from zope.interface import implements
# from AccessControl import getSecurityManager
# from Products.CMFCore.permissions import ModifyPortalContent
# from zope.component import getUtility
# from plone.i18n.normalizer.interfaces import INormalizer
# from plone.namedfile.field import NamedBlobImage
# from plone.namedfile.field import NamedBlobFile

# from plone.namedfile.file import NamedBlobImage as nbi
# from plone.namedfile.file import NamedBlobFile as nbf

# from collective import dexteritytextindexer
# from plone.directives import dexterity
# from plone.directives import form
# from z3c.form import button, field
# for events handlers
# from zope.lifecycleevent.interfaces import IObjectCreatedEvent
# from zope.lifecycleevent.interfaces import IObjectModifiedEvent
# END for events handlers
# import subprocess as sp
# import tempfile as tf
# from StringIO import StringIO
# from os import unlink

# from collective.abcmusic.abctune import IABCTune
# from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')


class midijsView(BrowserView):
    """Use MIDIjs for an ABCTune
    """

    """
    def update(self):
        context = self.context
    """

    def render(self):
        return ''

    def getJS_Song(self):
        TEMPLATE = '<script type="text/javascript" '
        TEMPLATE += 'class="javascript-settings">'
        TEMPLATE += "var song = '" + self.context.absolute_url()
        TEMPLATE += "/@@download/midi/" + self.context.midi.filename
        TEMPLATE += "'; </script>"
        return TEMPLATE
