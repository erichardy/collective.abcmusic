from zope.publisher.browser import BrowserView
import logging
from plone import api
from z3c.blobfile import file, image

from collective.abcmusic.abctune import _make_midi
from collective.abcmusic.abctune import _make_score
from collective.abcmusic.abctune import _make_PDFscore
from collective.abcmusic.abctune import addQ
from collective.abcmusic.abctune import addTuneType

from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')

class updateTune(BrowserView):
    """ AJAX method/view"""
    def __call__(self , abctext , abctuneURL):
        ## logger.info("dans __call_ de updateMTune:")
        abctune = api.content.get(path=abctuneURL)
        abctune.abc = abctext
        addTuneType(abctune)
        _make_midi(abctune)
        _make_score(abctune)
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