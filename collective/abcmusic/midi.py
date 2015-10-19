import logging
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import INormalizer
from plone.namedfile.file import NamedBlobFile as nbf

import subprocess as sp
import tempfile as tf
from StringIO import StringIO
from os import unlink

# from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')


def _make_midi(context):
    """
    peut etre utile : http://stackoverflow.com/questions/12298136/\
    dynamic-source-for-plone-dexterity-relationlist
    pour les donnees binaires : http://plone.org/products/dexterity/\
    documentation/manual/developer-manual/advanced/files-and-images
    """
    abc = context.abc
    abctemp = tf.NamedTemporaryFile(mode='w+b',
                                    suffix='.abc',
                                    delete=False).name
    fabctemp = open(abctemp, 'w')
    for l in abc:
        fabctemp.write(l)
    fabctemp.write('\n\n')
    fabctemp.close()
    miditemp = tf.NamedTemporaryFile(mode='w+b',
                                     suffix='.mid',
                                     delete=False).name
    p = sp.Popen(["abc2midi", abctemp, '-o', miditemp],
                 stdout=sp.PIPE,
                 stderr=sp.PIPE
                 )
    p.wait()
    iomidi = StringIO()
    fmiditemp = open(miditemp, 'r')
    buffmidi = fmiditemp.read()
    iomidi.write(buffmidi)

    title = context.title
    normalizer = getUtility(INormalizer)
    normalizedTitle = normalizer.normalize(title, locale='fr')
    midiFilename = unicode(normalizedTitle + '.mid')
    midiData = iomidi.getvalue()
    midiContentType = u'audio/mid'
    blobMidi = nbf(midiData,
                   contentType=midiContentType,
                   filename=midiFilename
                   )
    context.midi = blobMidi

    output, errors = p.communicate()
    # logger.info(errors)
    # logger.info(output)
    unlink(abctemp)
    unlink(miditemp)
    return output
