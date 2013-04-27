from zope.publisher.browser import BrowserView
import logging
from plone import api

from collective.abcmusic.abctune import _make_score
from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')

class updateScore(BrowserView):
    def __call__(self , abctext , abctuneURL):
        logger.info("dans __call_ de updateScore:" + abctext)
        abctune = api.content.get(path=abctuneURL)
        abctune.abc = abctext
        _make_score(abctune)
        # import pdb;pdb.set_trace()
        return True
