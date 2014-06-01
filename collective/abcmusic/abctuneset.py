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
from collective.abcmusic.abctune import removeNonAscii
from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')


class IABCTuneSet(form.Schema):
    form.omitted('abc')
    abc = schema.Text(title=_(u"Tune Set abc"),
                      description=_(u'The tunes set in abc format'),)

    form.omitted('score')
    score = NamedBlobImage(title=_(u"Score"),
                           description=
                                _(u'The score of the tunes set as png image'),
                           required=False,)

    form.omitted('pdfscore')
    pdfscore = NamedBlobFile (
            title = _(u"PDF Score"),
            description = _(u'The score of the tunes set as PDF'),
            required = False,
        )

    form.omitted('midi')
    midi = NamedBlobFile (
            title = _(u"Midi"),
            description = _(u'Midi sound of the tunes set'),
            required = False,
        )

    form.omitted('sound')
    sound = NamedBlobFile (
            title = _(u"sound"),
            description = _(u'The mp3 sound of the tunes set'),
            required = False,
        )



class abctuneset(Container):
    grok.implements(IABCTuneSet)


class View(grok.View):
    grok.context(IABCTuneSet)
    grok.require('zope2.View')
    
    def javascript(self):
        js = u"""<script type="text/javascript">\n"""
        js += u'tuneModified = ' + _(u"'The tune was modified... continue ?'") + u';\n'
        js += u'var uuid = "' + api.content.get_uuid(self.context) + '";\n'
        js += u'</script>'
        # import pdb;pdb.set_trace()
        return js


"""
see : http://docs.plone.org/external/plone.app.dexterity/docs/advanced/event-handlers.html
zope.lifecycleevent.interfaces.IObjectModifiedEvent
fired by the standard edit form when an object has been modified.
also fired when 
- an object position in the container is changed
- a new object is created in the container
- an object is removed
"""
@grok.subscribe(IABCTuneSet, IObjectModifiedEvent)
def modifAbcTuneSet(context , event):
    logger.info('IABCTuneSet, IObjectModifiedEvent')
    abcTunes = [abctune
                for abctune in event.object.objectValues()
                if abctune.portal_type == 'abctune']
    abc = ''
    for tune in abcTunes:
        abc += removeNonAscii(tune.abc)
        abc += '\n'
    context.abc = abc
    # import pdb;pdb.set_trace()

"""
To create the abc of the set :
- create the title (T:) from the titles and remove secondary T: fields
- remove X: except for the first
- analize the parts P: in order to play each tune as described in the according P:
- remove the secondary parts (P:B,...) from tunes
- set a part to each tune : first == P:A , second == P:B , etc...
not allowed in tune body : R: Z: 
- remove unnecessary headers (D: Z:) ???
- Q: must not be the first header of a secondary just after the previous tune
"""

