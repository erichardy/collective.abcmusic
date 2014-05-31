import logging
from five import grok
from plone import api
from plone.namedfile.interfaces import HAVE_BLOBS
from zope import schema
from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import INormalizer
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.field import NamedBlobFile

from plone.namedfile.file import NamedBlobImage as nbi
from plone.namedfile.file import NamedBlobFile as nbf

from collective import dexteritytextindexer
from plone.directives import dexterity
from plone.dexterity.content import Container
from plone.directives import form
from z3c.form import button, field
# for events handlers
from zope.lifecycleevent.interfaces import IObjectCreatedEvent, IObjectModifiedEvent
# END for events handlers
import subprocess as sp
import tempfile as tf
from StringIO import StringIO
from os import unlink

from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')


class IABCTuneSet(form.Schema):
    pass

class abctuneset(Container):
    grok.implements(IABCTuneSet)

