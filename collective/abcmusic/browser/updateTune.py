from zope.publisher.browser import BrowserView
import logging
from plone import api
from z3c.blobfile import file, image

from collective.abcmusic.abctune import _make_midi
from collective.abcmusic.abctune import _make_score
from collective.abcmusic.abctune import _make_PDFscore

from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')

class updateTune(BrowserView):
    def __call__(self , abctext , abctuneURL):
        logger.info("dans __call_ de updateMTune:")
        abctune = api.content.get(path=abctuneURL)
        abctune.abc = abctext
        _make_midi(abctune)
        _make_score(abctune)
        # _make_PDFscore(abctune)
        # import pdb;pdb.set_trace()
        return 1

class currentScore(BrowserView):
    """ TODO """
    def __call__(self, abctuneURL):
        abctune = api.content.get(path=abctuneURL)
        height = abctune.score._height
        width = abctune.score._width
        # import pdb;pdb.set_trace()
        # score = abctune.score.open().read()
        # return 'data:image/png;' + str(score)
        retour = '<img src="' + abctune.absolute_url() + '/@@download/score/'
        retour = retour +  abctune.score.filename
        retour = retour + '" height="' + str(height) + '" width="' + str(width) + '">'
        return retour

class currentMidi(BrowserView):
    """ TODO """
    def __call__(self, abctuneURL):
        abctune = api.content.get(path=abctuneURL)
        # import pdb;pdb.set_trace()
        retour = '<embed id="abctuneMidi" height="30" autostart="false" controller="true" autoplay="true"'
        retour = retour + ' src="' + abctune.absolute_url() + '/@@download/midi/' + abctune.midi.filename + '"'
        retour = retour + ' type="audio/mid"> </embed>'            
        return retour