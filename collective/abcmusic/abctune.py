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
        self.context.midi.filename = u'MidiFicher.mid'
        self.context.midi.contentType = u'audio/mid'
        # pour mp3 : u'audio/mpeg'
        output, errors = p.communicate()
        unlink(abctemp)
        # import pdb;pdb.set_trace()
        # unlink(miditemp)
        return output
        
        
    