from zope.publisher.browser import BrowserView
import logging
from plone import api
# from z3c.blobfile import file, image
from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent

from collective.abcmusic.abctune import _make_midi
from collective.abcmusic.abctune import _make_score
from collective.abcmusic.abctune import _make_PDFscore
from collective.abcmusic.abctune import addQ
from collective.abcmusic.abctune import addTuneType
from collective.abcmusic.abctune import addOrigins
from collective.abcmusic.mp3 import _make_mp3

from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')

class updateTune(BrowserView):
    """ AJAX method/view"""
    def __call__(self , abctext , abctuneURL, makeMP3):
        abctune = api.content.get(path=abctuneURL)
        sm = getSecurityManager()
        if not sm.checkPermission(ModifyPortalContent, abctune):
            return
        abctune.abc = abctext
        addTuneType(abctune)
        addOrigins(abctune)
        _make_midi(abctune)
        _make_score(abctune)
        if makeMP3 != '0':
            _make_mp3(abctune)
        # import pdb;pdb.set_trace()
        return 1

class currentScore(BrowserView):
    def __call__(self, abctuneURL):
        abctune = api.content.get(path=abctuneURL)
        height = abctune.score._height
        width = abctune.score._width
        retour = '<img src="' + abctune.absolute_url() + '/@@download/score/'
        retour = retour +  abctune.score.filename
        retour = retour + '" height="' + str(height) + '" width="' + str(width) + '">'
        return retour

class currentMidi(BrowserView):
    def __call__(self, abctuneURL):
        abctune = api.content.get(path=abctuneURL)
        retour = '<embed id="abctuneMidi" height="30" autostart="false" controller="true" autoplay="true"'
        retour = retour + ' src="' + abctune.absolute_url() + '/@@download/midi/' + abctune.midi.filename + '"'
        retour = retour + ' type="audio/mid"> </embed>'            
        return retour

class currentMP3(BrowserView):
    def __call__(self, abctuneURL):
        abctune = api.content.get(path=abctuneURL)
        retour = '<embed id="abctuneMP3" height="30" autostart="false" controller="true" autoplay="true"'
        retour = retour + ' src="' + abctune.absolute_url() + '/@@download/sound/' + abctune.sound.filename + '"'
        retour = retour + ' type="audio/mp3"> </embed>'            
        return retour