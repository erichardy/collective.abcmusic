import logging

from plone.namedfile.file import NamedBlobFile as nbf

import subprocess as sp
import tempfile as tf
from StringIO import StringIO
from os import unlink

from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')


def _make_mp3(context):

    midi = context.midi
    mididata = midi.data
    miditemp = tf.NamedTemporaryFile(mode='w+b',
                                     suffix='.mid', delete=False).name
    fmiditemp = open(miditemp, 'w')
    fmiditemp.write(mididata)
    fmiditemp.close()

    aifftemp = tf.NamedTemporaryFile(mode='w+b',
                                     suffix='.aiff', delete=False).name
    timidity = ["timidity",
                '-A 400',
                '-EFchorus=2,50',
                '-EFreverb=2',
                miditemp,
                '-o', aifftemp,
                '-Oa']

    p = sp.Popen(timidity, stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    output, errors = p.communicate()
    logger.info('in _make_mp3')
    logger.info(errors)
    logger.info(output)
    #
    mp3temp = tf.NamedTemporaryFile(mode='w+b',
                                    suffix='.mp3', delete=False).name
    lame = ["lame", '--cbr', '-b 32', '-f', '--quiet', aifftemp, mp3temp]

    p = sp.Popen(lame, stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()

    output, errors = p.communicate()
    # logger.info(errors)
    # logger.info(output)
    #
    iomp3 = StringIO()
    fmp3temp = open(mp3temp, 'r')
    buff_mp3 = fmp3temp.read()
    fmp3temp.close()
    iomp3.write(buff_mp3)
    #
    MP3Filename = u'sound.mp3'
    MP3Data = iomp3.getvalue()
    MP3ContentType = u'audio/mp3'
    blobMP3 = nbf(MP3Data, contentType=MP3ContentType, filename=MP3Filename)
    context.sound = blobMP3
    unlink(miditemp)
    unlink(aifftemp)
    unlink(mp3temp)

    return output, errors
