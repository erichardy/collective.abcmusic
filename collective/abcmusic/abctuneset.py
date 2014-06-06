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
from zope.component.interfaces import IObjectEvent
from zope.component.interfaces import ObjectEvent
from zope.event import notify
# END for events handlers
import subprocess as sp
import tempfile as tf
from StringIO import StringIO
from os import unlink
import re
from collective.abcmusic.utils import removeNonAscii
from collective.abcmusic.mp3 import _make_mp3
from collective.abcmusic.score import _make_score
from collective.abcmusic.midi import _make_midi
from collective.abcmusic.events import ITuneInTuneSetModified

from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')

"""
Each tune in a set must not have more than one part (P:), so two tags P:
- the first in the file to indicate how many times to play this tune
- the second, just before the note which is mandatory when a first P: tells
how many times to play the tune. 
If it has no part, it is assumed to be played only one time.
If those rules are not respected, the result is really uncertain... 
"""

class IABCTuneSet(form.Schema):
    
    form.omitted('combinedTitle')
    combinedTitle = schema.TextLine(
                    title=_(u"combined set title"),
                    description=_(u"this title depends of the tunes titles"),
                    )
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

def getFirstTitle(abcText):
    # because T: is mandatory, no more verifications
    tabc = abcText.split('T:')
    title = tabc[1].split('\n')[0].strip()
    return removeNonAscii(title)

# remove undesirable headers D: R: Z: ...
def cleanupHeaders(abcText):
    lines = abcText.split('\n')
    cleanedABC = []
    headersToRemove = ['D:','R:','S:','X:','Z:']
    for line in lines:
        if not line[:2] in headersToRemove:
            cleanedABC.append(line)
    return ('\n').join(cleanedABC)

"""
We re-organize the abc :
1/ remove undesirable headers
2/ comments first (they are also MIDI instructions)
3/ keep useful headers
4/ memorize only the first P:
%%QMLKP
"""
def reorgenize(abcText, part):
    abcText = cleanupHeaders(removeNonAscii(abcText))
    usefulHeaders = ['P:','Q:','M:','L:','K:','C:','T:']
    comments = []
    newABCTextLines = []
    Q = M = L = K = T = Parts = ''
    for line in abcText.split('\n'):
        if line[:1] == '%':
            comments.append(line.strip('\r'))
            # logger.info(line)
            # import pdb;pdb.set_trace()
        if line[:2] == 'T:':
            T = line + '\n'
        if line[:2] == 'Q:':
            Q = line + '\n'
        if line[:2] == 'M:':
            M = line + '\n'
        if line[:2] == 'L:':
            L = line + '\n'
        if line[:2] == 'K:':
            K = line + '\n'
        if line[:2] == 'P:':
            if Parts == '':
                Parts = line.split(':')[1].strip()
        if (line[:1] != '%' and line[:2] not in usefulHeaders):
            newABCTextLines.append(line)
    headers = '\n'.join(comments)
    headers += '\n' + T + Q + M + L + K
    headers += 'P:' + part + '\n'
    newABCText = headers
    newABCText += '\n'.join(newABCTextLines)
            
    # if ther is no P: header, we play only one time this tune
    if Parts == '':
        Parts = part
    else:
        Parts = part * len(Parts)
    # logger.info(newABCText)
    # logger.info('---------')
    # import pdb;pdb.set_trace()
    return newABCText , Parts

def aff(abc):
    aabc = cleanupHeaders(removeNonAscii(abc))
    l = []
    for line in aabc.split('\n'):
        logger.info(line)
        l.append(line)
    logger.info(l)
        
"""
see : http://docs.plone.org/external/plone.app.dexterity/docs/advanced/event-handlers.html
zope.lifecycleevent.interfaces.IObjectModifiedEvent
fired by the standard edit form when an object has been modified.
also fired when 
- an object position in the container is changed
- a new object is created in the container
- an object is removed
"""

def updateTuneSet(context, event):
    logger.ingo(event.object.portal_type)
    partsTags = ['A','B','C','D','E','F','G','H','I','J']
    num_parts = 0
    P_header = 'P:'
    abcTunes = [abctune
                for abctune in event.object.objectValues()
                if abctune.portal_type == 'abctune']
    abc = ''
    combinedTitle = ''
    for tune in abcTunes:
        combinedTitle += getFirstTitle(tune.abc)
        nbtunes = len(abcTunes) - 1
        if abcTunes.index(tune) < nbtunes:
            combinedTitle += ' / '
        # aff (tune.abc)
        # return
        abcreorgenized , parts = reorgenize(tune.abc, partsTags[num_parts])
        num_parts += 1
        P_header += parts
        abc += abcreorgenized
        
    context.combinedTitle = 'T: ' + combinedTitle
    context.abc = 'X:1\n' + context.combinedTitle + '\n'
    context.abc += P_header + '\n'
    context.abc += abc
    _make_midi(context)
    _make_score(context)

@grok.subscribe(IABCTuneSet, IObjectModifiedEvent)
def modifAbcTune(context , event):
    updateTuneSet(context, event)
    # logger.info('IABCTuneSet, IObjectModifiedEvent')
    # logger.info(combinedTitle)
    # import pdb;pdb.set_trace()

"""
To create the abc of the set :
- create the title (T:) from the titles and remove secondary T: fields
- remove X: except for the first
- analyze the parts P: in order to play each tune as described in the according P:
- remove the secondary parts (P:B,...) from tunes
- set a part to each tune : first == P:A , second == P:B , etc...
not allowed in tune body : R: Z: 
- remove unnecessary headers (D: Z:) ???
- Q: must not be the first header of a secondary just after the previous tune

"""

@grok.subscribe(IABCTuneSet, ITuneInTuneSetModified)
def tuneInTuneSetModified(context, event):
    logger.info('tuneInTuneSetModified Event')
    updateTuneSet(context, event)
