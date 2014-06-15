
import logging
from zope.publisher.browser import BrowserView
from zope.component.hooks import getSite
from collective.abcmusic.mp3 import _make_mp3

logger = logging.getLogger('collective.abcmusic')

class createAllMP3(BrowserView):

    def __call__(self):
        context = self.context
        folder_path = '/'.join(context.getPhysicalPath())
        site = getSite()
        catalog = site.portal_catalog
        results = catalog.searchResults(
                  portal_type = 'abctune',
                  path = {'query': folder_path, 'depth': 1},
                  )
        for result in results:
            tune = result.getObject()
            if not tune.sound:
                logger.info('Create MP3 for : ' + tune.title)
                _make_mp3(tune)
        return
