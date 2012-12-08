import logging
from five import grok
from zope import schema
from plone.namedfile.field import NamedImage , NamedBlobImage
from plone.namedfile.field import NamedFile , NamedBlobFile
from plone.directives import form
import subprocess as sp
import tempfile as tf
from StringIO import StringIO
import datetime
from os import unlink

from collective.abcmusic import _

# DateTime : http://pypi.python.org/pypi/DateTime/3.0.2

logger = logging.getLogger('collective.abcmusic')

class IABCTune(form.Schema):
    title = schema.TextLine(
            title=_(u"Tune name"),
        )
    description = schema.Text(
            title = _(u"Tune summary"),
            required = False,
        )
    form.primary('abc')
    abc = schema.Text(
            title = _(u"Tune abc"),
        )
    score = NamedBlobImage (
            title = _("Score"),
            description = _('The score of the tune'),
            required = False,
        )
    form.primary('midi')
    midi = NamedBlobFile (
            title = _("Midi"),
            description = _('Midi sound of the tune'),
            required = False,
        )
    form.primary('sound')
    sound = NamedBlobFile (
            title = _("sound"),
            description = _('The mp3 sound of the tune'),
            required = False,
        )
    abcTime = schema.Datetime(
            title = _(u'abc time'),
            description = _(u'the last modification time of abc'),
            required = False,
            )
    scoreTime = schema.Datetime(
            title = _(u'score time'),
            description = _(u'the last modification time of score'),
            required = False,
            )
    midiTime = schema.Datetime(
            title = _(u'midi time'),
            description = _(u'the last modification time of midi'),
            required = False,
            )
    soundTime = schema.Datetime(
            title = _(u'sound time'),
            description = _(u'the last modification time of sound'),
            required = False,
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

@form.default_value(field=IABCTune['abcTime'])
def abcTimeDefaultValue(data):
    # http://docs.python.org/2.6/whatsnew/2.3.html#date-time-type
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.now()

@form.default_value(field=IABCTune['scoreTime'])
def scoreTimeDefaultValue(data):
    # http://docs.python.org/2.6/whatsnew/2.3.html#date-time-type
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.now() - datetime.timedelta(1)

@form.default_value(field=IABCTune['midiTime'])
def midiTimeDefaultValue(data):
    # http://docs.python.org/2.6/whatsnew/2.3.html#date-time-type
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.now() - datetime.timedelta(1)

@form.default_value(field=IABCTune['soundTime'])
def soundTimeDefaultValue(data):
    # http://docs.python.org/2.6/whatsnew/2.3.html#date-time-type
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.now() - datetime.timedelta(1)


class View(grok.View):
    grok.context(IABCTune)
    grok.require('zope2.View')
    
    def make_midi(self):
        """
        peut etre utile : http://stackoverflow.com/questions/12298136/dynamic-source-for-plone-dexterity-relationlist
        pour les donnees binaires : http://plone.org/products/dexterity/documentation/manual/developer-manual/advanced/files-and-images
        """
        context = self.context
        if context.midiTime and (context.midiTime > context.abcTime):
            """ We do nothing, it's done
            """
            logger.info("midi plus recent que abc")
            return
        abc = context.abc
        abctemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.abc', delete = False).name
        fabctemp = open(abctemp , 'w')
        for l in abc:
            fabctemp.write(l)
        fabctemp.write('\n\n')
        fabctemp.close()
        miditemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.midi', delete = False).name
        p = sp.Popen(["abc2midi", abctemp,'-o', miditemp], stdout=sp.PIPE, stderr=sp.PIPE)
        p.wait()
        iomidi = StringIO()
        fmiditemp = open(miditemp , 'r')
        buffmidi = fmiditemp.read()
        iomidi.write(buffmidi)
        import pdb;pdb.set_trace()
        # logger.info(len(iomidi.getvalue()))
        self.context.midi.data = iomidi.getvalue()
        context.midi.filename = u'MidiFichier.mid'
        context.midi.contentType = u'audio/mid'
        context.midiTime = datetime.datetime.now()
        # pour mp3 : u'audio/mpeg'
        output, errors = p.communicate()
        unlink(abctemp)
        unlink(miditemp)
        # import pdb;pdb.set_trace()
        return output
        
    def make_score(self):
        context = self.context
        abc = context.abc
        if context.scoreTime and (context.scoreTime > context.abcTime):
            """ We do nothing, it's done
            """
            logger.info("score plus recent que abc")
            return
        
        abctemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.abc', delete = False).name
        fabctemp = open(abctemp , 'w')
        for l in abc:
            fabctemp.write(l)
        fabctemp.write('\n\n')
        fabctemp.close()
        pstemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.ps', delete = False).name
        p = sp.Popen(["abcm2ps", abctemp,'-O', pstemp], stdout=sp.PIPE, stderr=sp.PIPE)
        p.wait()
        # convert ${PSFILE} -filter Catrom  -resize 600 $PNG"
        pngtemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.png', delete = False).name
        p = sp.Popen(["convert", pstemp,'-filter', 'Catrom', '-resize', '600', pngtemp], stdout=sp.PIPE, stderr=sp.PIPE)
        p.wait()
        io_png = StringIO()
        fpngtemp = open(pngtemp ,'r')
        buff_score = fpngtemp.read()
        io_png.write(buff_score)
        context.score.data = io_png.getvalue()
        context.score.filename = u'ScoreFichier.png'
        context.score.contentType = u'image/png'
        context.scoreTime = datetime.datetime.now()
        output, errors = p.communicate()
        unlink(abctemp)
        unlink(pstemp)
        unlink(pngtemp)
        # import pdb;pdb.set_trace()
        return output
    