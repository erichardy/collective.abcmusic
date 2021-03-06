import logging
from five import grok
from plone import api
# from plone.namedfile.interfaces import HAVE_BLOBS
from zope import schema
from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent
# from zope.component import getUtility
# from plone.i18n.normalizer.interfaces import INormalizer
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.field import NamedBlobFile

# from plone.namedfile.file import NamedBlobImage as nbi
# from plone.namedfile.file import NamedBlobFile as nbf

from collective import dexteritytextindexer
# from plone.directives import dexterity
from plone.directives import form
# from z3c.form import button, field
# for events handlers
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.event import notify
from collective.abcmusic.events import ITuneInTuneSetModified
from collective.abcmusic.events import TuneInTuneSetModified
from collective.abcmusic.abctuneset import updateTuneSet
# END for events handlers
# import subprocess as sp
# import tempfile as tf
# from StringIO import StringIO
# from os import unlink

# from collective.abcmusic.mp3 import _make_mp3
from collective.abcmusic.score import _make_score
from collective.abcmusic.midi import _make_midi
from collective.abcmusic.utils import removeNonAscii
from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')

tunearea_title = _(u"The area from which the tune is from")
tunearea_desc = _(u"More detailed origin of the tune, from O: field")
tunecountry_title = u"The origin country of the tune, "
tunecountry_title += u"from first part of O: field"
tunecountry_title = _(tunecountry_title)
score_desc = _(u'The score of the tune as png image')


class IABCTune(form.Schema):

    dexteritytextindexer.searchable('abc')
    form.primary('abc')
    abc = schema.Text(title=_(u"Tune abc"),
                      description=_(u'The tune in abc format'),)

    dexteritytextindexer.searchable('tunekeys')
    form.omitted('tunekeys')
    tunekeys = schema.List(title=u'keys',
                           description=u'set by abc content',
                           required=False,
                           value_type=schema.TextLine(required=False),
                           )

    dexteritytextindexer.searchable('tunetype')
    form.omitted('tunetype')
    tunetype = schema.TextLine(title=_(u"The type of the tune"),
                               description=_(u"from the field R:"),
                               required=False,
                               )
    # NOTE: as specified in the v2.1 standard, A: field is deprecated
    # so, only O: is used to specified country and areas... separated
    # by ';'
    dexteritytextindexer.searchable('tunearea')
    form.omitted('tunearea')
    tunearea = schema.TextLine(title=tunearea_title,
                               description=tunearea_desc,
                               required=False,
                               )
    dexteritytextindexer.searchable('tunecountry')
    form.omitted('tunecountry')
    tunecountry = schema.TextLine(title=tunecountry_title,
                                  description=_(u"The country"),
                                  required=False,
                                  )

    form.omitted('score')
    score = NamedBlobImage(title=_(u"Score"),
                           description=score_desc,
                           required=False,)

    form.omitted('pdfscore')
    pdfscore = NamedBlobFile(title=_(u"PDF Score"),
                             description=_(u'The score of the tune as PDF'),
                             required=False,
                             )

    form.omitted('midi')
    midi = NamedBlobFile(title=_(u"Midi"),
                         description=_(u'Midi sound of the tune'),
                         required=False,
                         )
    form.omitted('sound')
    sound = NamedBlobFile(title=_(u"sound"),
                          description=_(u'The mp3 sound of the tune'),
                          required=False,
                          )


@form.default_value(field=IABCTune['abc'])
def abcDefaultValue(data):
    # http://docs.python.org/2.6/whatsnew/2.3.html#date-time-type
    # To get hold of the folder, do: context = data.context
    tune = """
X:1
T:Ashplant, The
%%MIDI chordvol 30
%%MIDI bassvol 30
R:reel
Q:180
P:AAAAA
D:Noel Hill & Tony McMahon: 'I gCnoc na Gra'i
Z:id:hn-reel-285
M:C|
K:Edor
P:A
|:"Em"BE E2 "G"BAGA|"Em"BE E2  "G"G3A|1 "Em"BE E2 BABd|
"G"gedB "D"A2GA:|2  "Em"B3A "Bm"Bd ef|"G"gedB "D"A2GA|
|:"Em"B2eB "Bm"fBeB| "Em"B2ed BAGA|1 "Em"B2eB  "D"f3d|
"Em"efdB "D"A2GA:|2 "Bm"Bd ef  "G"g3a|"G"gedB "D"A2GA||
"""
    return tune


# for hidden fields, see : http://packages.python.org/z3c.form/\
# form.html#hidden-fields
# to use in the add and edit forms
class View(grok.View):
    grok.context(IABCTune)
    grok.require('zope2.View')

    """
    def __call__(self):
        return
        import pdb;pdb.set_trace()
    """
    def abcAutorized(self):
        context = self.context
        sm = getSecurityManager()
        if not sm.checkPermission(ModifyPortalContent, context):
            return False
        return True

    def javascript(self):
        auth = self.abcAutorized()
        authjs = u'true'
        if not auth:
            authjs = u'false'

        js = u"""<script type="text/javascript">\n"""
        js += u'tuneModified = ' + _(u"'The tune was modified... continue ?'")
        js += u';\n'
        js += u'var uuid = "' + api.content.get_uuid(self.context) + '";\n'
        js += u'var auth = ' + authjs + ';\n'
        js += u'</script>'
        # import pdb;pdb.set_trace()
        return js

    def sujbectsStr(self):
        subjects = self.context.subject
        subject_str = ''
        for s in subjects:
            subject_str += s + ', '
        return subject_str.strip(', ')


def addQ(context):
    abc = context.abc
    if len(abc.split('Q:')) == 1:
        labc = abc.split('\n')
        labc.insert(1, 'Q:100')
        abc = ('\n').join(labc)
        context.abc = abc


def addTuneType(context):
    abc = context.abc
    labc = abc.split('R:')
    if len(labc) != 1:
        tunetype = labc[1].split('\n')[0]
        context.tunetype = tunetype.strip().lower()
    else:
        context.tunetype = "unknown"


def addOrigins(context):
    abc = context.abc
    labc = abc.split('O:')
    if len(labc) > 1:
        tuneOrigins = labc[1].split('\n')[0].split(';')
        context.tunecountry = tuneOrigins[0]
        if len(tuneOrigins) != 1:
            context.tunearea = ';'.join(tuneOrigins[1:])
    else:
        context.tunearea = "unknown"


def addKeys(context):
    abc = context.abc
    keys = []
    for line in abc.split('\n'):
        if line[:2] == 'K:':
            key = line.split(':')[1].strip()
            if key not in keys:
                keys.append(key)
    context.tunekeys = keys


@grok.subscribe(IABCTune, IObjectCreatedEvent)
def newAbcTune(context, event):
    try:
        context.abc = removeNonAscii(context.abc)
        addQ(context)
        addTuneType(context)
        addOrigins(context)
        addKeys(context)
        _make_midi(context)
        _make_score(context)
        # _make_mp3(context)
        logger.info("abc created !")
    except:
        logger.info("abctune not created...")


@grok.subscribe(IABCTune, IObjectModifiedEvent)
def updateAbcTune(context, event):
    try:
        context.abc = removeNonAscii(context.abc)
        addQ(context)
        addTuneType(context)
        addOrigins(context)
        addKeys(context)
        _make_midi(context)
        _make_score(context)
        parent = context.aq_parent

        if parent.portal_type == 'abctuneset':
            log = '(IObjectModifiedEvent)abctune.updateAbcTune '
            log += parent.portal_type
            logger.info(log)
            notify(TuneInTuneSetModified(context))
        # _make_mp3(context)

    except:
        logger.info("updateAbcTune : abctune not modified...")
    # logger.info("abc edited/modified !")


@grok.subscribe(IABCTune, ITuneInTuneSetModified)
def tuneInTuneSetModified(context, event):
    logger.info('(ITuneInTuneSetModified)abctune.tuneInTuneSetModified Event')
    updateTuneSet(context.aq_parent)


# for addForm, see : https://pypi.python.org/pypi/plone.directives.form/1.1
# class Add(dexterity.AddForm):
#    grok.name('abctune')
#    grok.template('addAbcTune')
