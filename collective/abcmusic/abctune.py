import logging
from five import grok
from plone.namedfile.interfaces import HAVE_BLOBS
from zope import schema
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import INormalizer
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.field import NamedBlobFile
from collective import dexteritytextindexer
from z3c.blobfile import file, image
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


class IABCTune(form.Schema):
    title = schema.TextLine(title=_(u"Tune name"),)

    description = schema.Text(title=_(u"Tune summary"),
                              required=False,)

    dexteritytextindexer.searchable('abc')
    form.primary('abc')
    abc = schema.Text(title=_(u"Tune abc"),
                      description=_(u'The tune in abc format'),)

    form.omitted('score')
    score = NamedBlobImage(title=_(u"Score"),
                           description=
                                _(u'The score of the tune as png image'),
                           required=False,)

    form.omitted('pdfscore')
    pdfscore = NamedBlobFile (
            title = _(u"PDF Score"),
            description = _(u'The score of the tune as PDF'),
            required = False,
        )

    form.omitted('midi')
    midi = NamedBlobFile (
            title = _(u"Midi"),
            description = _(u'Midi sound of the tune'),
            required = False,
        )
    form.omitted('sound')
    sound = NamedBlobFile (
            title = _(u"sound"),
            description = _(u'The mp3 sound of the tune'),
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

# for hidden fields, see : http://packages.python.org/z3c.form/form.html#hidden-fields
# to use in the add and edit forms
class View(grok.View):
    grok.context(IABCTune)
    grok.require('zope2.View')
    
    """
    def __call__(self):
        return
        import pdb;pdb.set_trace()
    """
        
def _make_midi(context):
    """
    peut etre utile : http://stackoverflow.com/questions/12298136/dynamic-source-for-plone-dexterity-relationlist
    pour les donnees binaires : http://plone.org/products/dexterity/documentation/manual/developer-manual/advanced/files-and-images
    """
    abc = context.abc
    abctemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.abc', delete = False).name
    fabctemp = open(abctemp , 'w')
    for l in abc:
        fabctemp.write(l)
    fabctemp.write('\n\n')
    fabctemp.close()
    miditemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.mid', delete = False).name
    p = sp.Popen(["abc2midi", abctemp,'-o', miditemp], stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    iomidi = StringIO()
    fmiditemp = open(miditemp , 'r')
    buffmidi = fmiditemp.read()
    iomidi.write(buffmidi)

    blobMidi = file.File()
    title = context.title
    normalizer = getUtility(INormalizer)
    normalizedTitle = normalizer.normalize(title, locale = 'fr')
    blobMidi.filename = normalizedTitle + '.mid'
    blobMidi.data = iomidi.getvalue()
    blobMidi.contentType = u'audio/mid'
    # pour mp3 : u'audio/mpeg'
    context.midi = blobMidi    
    output, errors = p.communicate()
    unlink(abctemp)
    unlink(miditemp)
    return output
        
def _make_score(context):
    # make score as png AND PDF
    abc = context.abc
    title = context.title
    normalizer = getUtility(INormalizer)
    normalizedTitle = normalizer.normalize(title, locale = 'fr')
    abctemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.abc', delete = False).name
    fabctemp = open(abctemp , 'w')
    for l in abc:
        fabctemp.write(l)
    fabctemp.write('\n\n')
    fabctemp.close()
    epstemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.eps', delete = False).name
    p = sp.Popen(["abcm2ps", abctemp,'-E -O', epstemp], stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    # convert ${PSFILE} -filter Catrom  -resize 600 $PNG"
    pngtemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.png', delete = False).name
    p = sp.Popen(["convert", epstemp.split('.eps')[0] + '001.eps' ,'-filter', 'Catrom', '-resize', '600', pngtemp], stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    iopng = StringIO()
    fpngtemp = open(pngtemp ,'r')
    buff_score = fpngtemp.read()
    iopng.write(buff_score)

    blobScore = image.Image()
    # blobScore.filename = u'ScoreFichier.png'
    blobScore.filename = normalizedTitle + '.png'
    blobScore.data = iopng.getvalue()
    blobScore.contentType = u'image/png'
    context.score = blobScore
    output, errors = p.communicate()
    ## logger.info(abctemp)
    
    pstemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.ps', delete = False).name
    p = sp.Popen(["abcm2ps", abctemp,'-O', pstemp], stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    pdftemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.pdf', delete = False).name
    pdf_create = sp.Popen(["ps2pdf", pstemp, pdftemp], stdout=sp.PIPE, stderr=sp.PIPE)
    pdf_create.wait()
    iopdf = StringIO()
    fpdftemp = open(pdftemp ,'r')
    buff_pdfscore = fpdftemp.read()
    iopdf.write(buff_pdfscore)
    blobPDF = file.File()
    # blobPDF.filename = u'PDF_File.pdf'
    blobPDF.filename = normalizedTitle + '.pdf'
    blobPDF.data = iopdf.getvalue()
    blobPDF.contentType = u'application/pdf'
    context.pdfscore = blobPDF
    ## logger.info(pdftemp)
    
    output, errors = pdf_create.communicate()
    
    unlink(abctemp)
    unlink(pstemp)
    unlink(pngtemp)
    unlink(pdftemp)
    return output

def _make_PDFscore(context):
    abc = context.abc
    abctemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.abc', delete = False).name
    fabctemp = open(abctemp , 'w')
    for l in abc:
        fabctemp.write(l)
    fabctemp.write('\n\n')
    fabctemp.close()
    pstemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.ps', delete = False).name
    p = sp.Popen(["ps2pdf", abctemp,'-O', pstemp], stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    # convert ${PSFILE} -filter Catrom  -resize 600 $PNG"
    pdftemp = tf.NamedTemporaryFile(mode='w+b', suffix = '.pdf', delete = False).name
    
    p = sp.Popen(["ps2pdf", pstemp, pdftemp], stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    iopdf = StringIO()
    fpdftemp = open(pdftemp ,'r')
    buff_score = fpdftemp.read()
    iopdf.write(buff_score)

    blobPDFScore = file.File()
    blobPDFScore.filename = u'PDFScoreFichier.pdf'
    blobPDFScore.data = iopdf.getvalue()
    blobPDFScore.contentType = u'application/pdf'
    context.pdfscore = blobPDFScore
    output, errors = p.communicate()
    ## logger.info('PDF: ' + abctemp)
    unlink(abctemp)
    unlink(pstemp)
    unlink(pdftemp)
    return output

def addQ(context):
    abc = context.abc
    if len(abc.split('Q:')) == 1:
        labc = abc.split('\n')
        labc.insert(1,'Q:100')
        abc = ('\n').join(labc)
        context.abc = abc

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

@grok.subscribe(IABCTune, IObjectCreatedEvent)
def newAbcTune(context , event):
    try:
        context.abc = removeNonAscii(context.abc)
        addQ(context)
        _make_midi(context)
        _make_score(context)
        ## logger.info("abc created !")
    except:
        logger.info("abctune not created...")
    # import pdb;pdb.set_trace()

@grok.subscribe(IABCTune, IObjectModifiedEvent)
def updateAbcTune(context , event):
    try:
        context.abc = removeNonAscii(context.abc)
        addQ(context)
        _make_midi(context)
        _make_score(context)
    except:
        logger.info("abctune not modified...")
    ## logger.info("abc edited/modified !")
    
    

    
