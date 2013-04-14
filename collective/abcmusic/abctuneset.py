import logging
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from five import grok
from plone.namedfile.interfaces import HAVE_BLOBS
from zope import schema
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.field import NamedBlobFile
from z3c.blobfile import file, image
from plone.directives import form, dexterity
from z3c.form import button, field
# for events handlers
from zope.lifecycleevent.interfaces import IObjectCreatedEvent,IObjectModifiedEvent
# END for events handlers
import subprocess as sp
import tempfile as tf
from StringIO import StringIO
import datetime
from collective.abcmusic.abctune import IABCTune

from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')

class IABCTuneSet(form.Schema):
    title = schema.TextLine(
            title=_(u"Tune set name"),
        )
    description = schema.Text(
            title = _(u"Tune set summary"),
            required = False,
        )

class View(grok.View):
    grok.context(IABCTuneSet)
    grok.require('zope2.View')

    def abctunesList(self):
        """Return a catalog search result of abctunes to show
        """

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        return catalog(portal_type = 'abctune',
	               path='/'.join(context.getPhysicalPath()),
	               sort_on='sortable_title')

