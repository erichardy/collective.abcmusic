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
    
    midi = context.midi
    mididata = midi.data
    miditemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.mid',delete = False).name
    fmiditemp = open(miditemp, 'w')
    fmiditemp.write(mididata)
    fmiditemp.close()
    
    aifftemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.aiff',delete = False).name
    timidity = ["timidity",'-A 400','-EFchorus=2,50','-EFreverb=2',miditemp ,'-o', aifftemp,'-Oa']
    
    p = sp.Popen(timidity, stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    output, errors = p.communicate()
    # logger.info(errors)
    # logger.info(output)
    #
    mp3temp = tf.NamedTemporaryFile(mode='w+b', suffix = '.mp3',delete = False).name
    lame = ["lame",'--cbr','-b 32','-f','--quiet',aifftemp, mp3temp]
    
    p = sp.Popen(lame, stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    
    output, errors = p.communicate()
    # logger.info(errors)
    # logger.info(output)
    #
    iomp3 = StringIO()
    fmp3temp = open(mp3temp,'r')
    buff_mp3 = fmp3temp.read()
    fmp3temp.close()
    iomp3.write(buff_mp3)
    #
    MP3Filename = u'sound.mp3'
    MP3Data = iomp3.getvalue()
    MP3ContentType =  u'audio/mp3'
    blobMP3 = nbf(MP3Data,contentType=MP3ContentType, filename=MP3Filename)
    context.sound = blobMP3
    unlink(miditemp)
    unlink(aifftemp)
    unlink(mp3temp)
    
    return output, errors
