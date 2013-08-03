from zope.publisher.browser import BrowserView
import logging
from plone import api

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
        return abctune.midi.filename
