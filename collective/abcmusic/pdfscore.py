import logging
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import INormalizer
from plone.namedfile.file import NamedBlobImage as nbi
from plone.namedfile.file import NamedBlobFile as nbf

import subprocess as sp
import tempfile as tf
from StringIO import StringIO
from os import unlink

from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')


def _make_PDFscore(context):
    abc = context.abc
    title = context.title
    normalizer = getUtility(INormalizer)
    normalizedTitle = normalizer.normalize(title, locale='fr')
    abctemp = tf.NamedTemporaryFile(mode='w+b',
                                    suffix='.abc', delete=False).name
    fabctemp = open(abctemp, 'w')
    for l in abc:
        fabctemp.write(l)
    fabctemp.write('\n\n')
    fabctemp.close()
    pstemp = tf.NamedTemporaryFile(mode='w+b',
                                   suffix='.ps', delete=False).name
    p = sp.Popen(["ps2pdf", abctemp, '-O', pstemp],
                 stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    # convert ${PSFILE} -filter Catrom  -resize 600 $PNG"
    pdftemp = tf.NamedTemporaryFile(mode='w+b',
                                    suffix='.pdf', delete=False).name

    p = sp.Popen(["ps2pdf", pstemp, pdftemp], stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    iopdf = StringIO()
    fpdftemp = open(pdftemp, 'r')
    buff_score = fpdftemp.read()
    iopdf.write(buff_score)
    """
    Must to be modified according to the other methods above...
    but this method is no longer used...
    """
    blobPDFScore = context.pdfscore
    blobPDFScore.filename = unicode(normalizedTitle + '.pdf')
    blobPDFScore.data = iopdf.getvalue()
    blobPDFScore.contentType = u'application/pdf'

    output, errors = p.communicate()
    # logger.info(errors)
    # logger.info(output)
    ## logger.info('PDF: ' + abctemp)
    unlink(abctemp)
    unlink(pstemp)
    unlink(pdftemp)
    return output
