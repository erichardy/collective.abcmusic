import logging
from five import grok
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

def _make_mp3(context):
    """if midi doesn't exists, we do nothing
    """
    midi = context.midi
    mididata = midi.data
    miditemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.mid',delete = False).name
    fmiditemp = open(miditemp, 'w')
    fmiditemp.write(mididata)
    import pdb;pdb.set_trace()
    aifftemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.aiff',delete = False).name
    p = sp.Popen(["timidity", miditemp,'-A 400 -EFchorus=2,50 -EFreverb=2' + ' miditemp ' + '-Oa', aifftemp], stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    output, errors = p.communicate()
    import pdb;pdb.set_trace()
    mp3temp = tf.NamedTemporaryFile(mode='w+b', suffix = '.mp3',delete = False).name
    p = sp.Popen(["lame", aifftemp,'--cbr -b 32 -f --quiet', mp3temp], stdout=sp.PIPE, stderr=sp.PIPE)
    output, errors = p.communicate()
    import pdb;pdb.set_trace()
    iomp3 = StringIO()
    fmp3temp = open(mp3temp,'w')
    buff_mp3 = fmp3temp.read()
    iomp3.write(buff_mp3)
    logger.info(mp3temp)
    MP3Filename = u'sound.mp3'
    MP3Data = iomp3.getvalue()
    MP3ContentType =  u'audio/mp3'
    blobMP3 = nbf(MP3Data,contentType=MP3ContentType, filename=MP3Filename)
    context.sound = blobMP3
    # unlink(miditemp)
    # unlink(aifftemp)
    # unlink(mp3temp)
    import pdb;pdb.set_trace()
    return output, errors
