from zope.publisher.browser import BrowserView
import logging
from plone import api

from collective.abcmusic.abctune import _make_midi
from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')

class updateMidi(BrowserView):
    def __call__(self , abctext , abctuneURL):
        logger.info("dans __call_ de updateMidi:" + abctext)
        abctune = api.content.get(path=abctuneURL)
        abctune.abc = abctext
        _make_midi(abctune)
        # import pdb;pdb.set_trace()
        return True
