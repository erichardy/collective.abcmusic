import logging
from zope.publisher.browser import BrowserView
from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')

title = _(u'abc_collection_view')

class abcCollectionView(BrowserView):
    pass

