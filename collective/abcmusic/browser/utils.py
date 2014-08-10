import logging
from zope.publisher.browser import BrowserView
from zope.component.hooks import getSite
from Products.CMFCore.interfaces import IFolderish

from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')


def doRecurse(location):
    for id, child in location.contentItems():
        # do something !
        logger.info('id:' + str(id))
        logger.info('child:' + str(child.portal_type))
        child.reindexObject()
        if IFolderish.providedBy(child):
            doRecurse(child)


class recurse(BrowserView):
    def __call__(self):
        context = self.context
        context.reindexObject()
        if IFolderish.providedBy(context):
            doRecurse(context)

