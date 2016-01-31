import logging
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import INormalizer
from plone.namedfile.file import NamedBlobImage as nbi
from plone.namedfile.file import NamedBlobFile as nbf

import subprocess as sp
import tempfile as tf
from StringIO import StringIO
from os import unlink

# from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')


def _make_score(context):
    """Make score as png AND PDF
    :param context: this method is always applied on an abctune
    :type context: abctune
    :returns:
    """
    # First, we create a file with abc text
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
    # then call abcm2ps to create an eps file
    epstemp = tf.NamedTemporaryFile(mode='w+b',
                                    suffix='.eps', delete=False).name
    p = sp.Popen(["abcm2ps", abctemp, '-E -O', epstemp],
                 stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    # with this eps, create the png score
    # convert ${PSFILE} -filter Catrom  -resize 600 $PNG"
    pngtemp = tf.NamedTemporaryFile(mode='w+b',
                                    suffix='.png', delete=False).name
    p = sp.Popen(["convert",
                  epstemp.split('.eps')[0] + '001.eps',
                  '-filter',
                  'Catrom',
                  '-resize',
                  '600',
                  pngtemp], stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    iopng = StringIO()
    fpngtemp = open(pngtemp, 'r')
    buff_score = fpngtemp.read()
    iopng.write(buff_score)

    scoreData = iopng.getvalue()
    scoreFilename = unicode(normalizedTitle + '.png')
    scoreContentType = u'image/png'
    # the png score is stored in the object (attr : score)
    blobScore = nbi(scoreData,
                    contentType=scoreContentType,
                    filename=scoreFilename)

    context.score = blobScore
    output, errors = p.communicate()
    logger.info(errors)
    logger.info(output)
    # logger.info(abctemp)
    # then create a ps file for PDF transform
    pstemp = tf.NamedTemporaryFile(mode='w+b',
                                   suffix='.ps', delete=False).name
    p = sp.Popen(["abcm2ps", abctemp,
                  '-O', pstemp],
                 stdout=sp.PIPE,
                 stderr=sp.PIPE
                 )
    p.wait()
    pdftemp = tf.NamedTemporaryFile(mode='w+b',
                                    suffix='.pdf', delete=False).name
    pdf_create = sp.Popen(["ps2pdf", pstemp, pdftemp],
                          stdout=sp.PIPE, stderr=sp.PIPE)
    pdf_create.wait()
    iopdf = StringIO()
    fpdftemp = open(pdftemp, 'r')
    buff_pdfscore = fpdftemp.read()
    iopdf.write(buff_pdfscore)
    # The PDF score is stored in the object (attr: pdfscore)
    PDFScoreFilename = unicode(normalizedTitle + '.pdf')
    PDFScoreData = iopdf.getvalue()
    PDFScoreContentType = u'application/pdf'
    blobPDFScore = nbf(PDFScoreData,
                       contentType=PDFScoreContentType,
                       filename=PDFScoreFilename)
    context.pdfscore = blobPDFScore
    logger.info(pdftemp)

    output, errors = pdf_create.communicate()
    # logger.info(errors)
    logger.info(epstemp)
    unlink(abctemp)
    unlink(pstemp)
    unlink(epstemp.split('.eps')[0] + '001.eps')
    unlink(epstemp)
    unlink(pngtemp)
    unlink(pdftemp)
    return output
