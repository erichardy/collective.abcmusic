from zope.publisher.browser import BrowserView
import logging
from plone import api
from zope.component.hooks import getSite
from plone.app.uuid.utils import uuidToObject
# from z3c.blobfile import file, image
from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent
from DateTime import DateTime
from datetime import datetime
from collective.abcmusic.midi import _make_midi
from collective.abcmusic.score import _make_score
from collective.abcmusic.pdfscore import _make_PDFscore
from collective.abcmusic.mp3 import _make_mp3

from collective.abcmusic.abctune import addTuneType
from collective.abcmusic.abctune import addOrigins
from collective.abcmusic.abctune import addKeys
from collective.abcmusic.abctuneset import updateTuneSet

from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic updateTune: ')


def removeViewInURL(url):
    """ OK if the tune name is not 'view' """
    l_url = url.split('/')
    if l_url[len(l_url) - 1] == 'view':
        l_url.pop()
        url = '/'.join(l_url)
    logger.info('update : ' + url)
    return url


class updateTune(BrowserView):
    """ AJAX method/view"""
    def __call__(self, abctext, uuid, makeMP3):
        # need to remove 'view' at the end if present
        abctune = uuidToObject(uuid)
        sm = getSecurityManager()
        if not sm.checkPermission(ModifyPortalContent, abctune):
            return
        abctune.abc = abctext
        addTuneType(abctune)
        addOrigins(abctune)
        addKeys(abctune)
        _make_midi(abctune)
        _make_score(abctune)

        # _make_PDFscore(abctune)
        if makeMP3 != '0':
            _make_mp3(abctune)
        # import pdb;pdb.set_trace()
        abctune.modification_date = DateTime()
        logger.info(abctune.modified())
        logger.info('"' + abctune.title + '" updated')
        parent = abctune.aq_parent
        if parent.portal_type == 'abctuneset':
            # logger.info('in updateTune.updateTune')
            updateTuneSet(parent)
        site = getSite()
        catalog = site.portal_catalog
        catalog.reindexObject(abctune)
        return 1


class currentScore(BrowserView):
    """ AJAX method/view"""
    def __call__(self, uuid):
        today = datetime.today()
        microsecond = today.microsecond
        abctune = uuidToObject(uuid)
        height = abctune.score._height
        width = abctune.score._width
        retour = '<img src="' + abctune.absolute_url() + '/@@download/score/'
        retour += abctune.score.filename
        retour += '/?' + str(microsecond)
        retour += '" height="' + str(height) + '" width="' + str(width) + '">'
        return retour


class currentPDFScore(BrowserView):
    """ AJAX method/view"""
    def __call__(self, uuid):
        abctune = uuidToObject(uuid)
        retour = '<a id="abctunePDFScore" '
        retour += 'href="' + abctune.absolute_url() + '/@@download/pdfscore/'
        retour += abctune.pdfscore.filename + '"'
        retour += ' target="_blank" type="application/pdf" >'
        retour += '<img src="pdf.png" /></a>'
        return retour


class currentMidi(BrowserView):
    """ AJAX method/view"""
    def __call__(self, uuid):
        abctune = uuidToObject(uuid)
        # retour = '<embed id="abctuneMidi" height="30" autostart="true" '
        # retour += controller="true" autoplay="true"'
        retour = '<embed id="abctuneMidi" height="30" autostart="false" '
        retour += 'controller="true" autoplay="false"'
        retour += ' src="' + abctune.absolute_url() + '/@@download/midi/'
        retour += abctune.midi.filename + '"'
        retour += ' type="audio/mid"> </embed>'
        return retour


class currentMP3(BrowserView):
    """ AJAX method/view"""
    def __call__(self, uuid):
        abctune = uuidToObject(uuid)
        retour = '<embed id="abctuneMP3" height="30" autostart="false" '
        retour += 'controller="true" autoplay="true"'
        retour += ' src="' + abctune.absolute_url() + '/@@download/sound/'
        retour += abctune.sound.filename + '"'
        retour += ' type="audio/mp3"> </embed>'
        return retour


class createMP3(BrowserView):
    """ AJAX method/view"""
    def __call__(self, abctext, uuid):
        abctune = uuidToObject(uuid)
        sm = getSecurityManager()
        if not sm.checkPermission(ModifyPortalContent, abctune):
            return
        abctune.abc = abctext
        _make_mp3(abctune)
        retour = '<embed id="abctuneMP3" height="30" autostart="false" '
        retour += 'controller="true" autoplay="true"'
        retour += ' src="' + abctune.absolute_url() + '/@@download/sound/'
        retour += abctune.sound.filename + '"'
        retour += ' type="audio/mp3"> </embed>'
        return retour
