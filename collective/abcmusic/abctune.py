import logging
from five import grok
from zope import schema
from plone.namedfile.field import NamedImage , NamedBlobImage
from plone.namedfile.field import NamedFile , NamedBlobFile
from plone.directives import form
import subprocess as sp
import tempfile as tf
from StringIO import StringIO

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
            description = _('The sound of the tune'),
            required = False,
        )

class View(grok.View):
    grok.context(IABCTune)
    grok.require('zope2.View')
    
    def make_midi(self):
        """
        peut etre utile : http://stackoverflow.com/questions/12298136/dynamic-source-for-plone-dexterity-relationlist
        pour les donnees binaires : http://plone.org/products/dexterity/documentation/manual/developer-manual/advanced/files-and-images
        """
        abc = self.context.abc
        
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
        # logger.info(len(iomidi.getvalue()))
        self.context.midi.data = iomidi.getvalue()
        self.context.midi.filename = u'MidiFichier.mid'
        self.context.midi.contentType = u'audio/mid'
        # pour mp3 : u'audio/mpeg'
        output, errors = p.communicate()
        unlink(abctemp)
        unlink(miditemp)
        # import pdb;pdb.set_trace()
        return output
        
    def make_score(self):
        abc = self.context.abc
        
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
        self.context.score.data = io_png.getvalue()
        self.context.score.filename = u'ScoreFichier.png'
        self.context.score.contentType = u'image/png'
        output, errors = p.communicate()
        unlink(abctemp)
        unlink(pstemp)
        unlink(pngtemp)
        import pdb;pdb.set_trace()
        return output
    