import logging
from zope.publisher.browser import BrowserView
from AccessControl import getSecurityManager
from Products.CMFCore import permissions
from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')

title = _(u'abc_collection_view')


class abcCollectionView(BrowserView):
    def itemEditable(self, item):
        editable = getSecurityManager().checkPermission(
                                    permissions.ModifyPortalContent,
                                    item.getObject())
        return editable
