# -*- coding: UTF-8 -*-
import logging
from zope.publisher.browser import BrowserView
from zope.component.hooks import getSite
from plone import api
logger = logging.getLogger('collective.abcmusic')


class getTunes(BrowserView):

    def getLocalTunes(self):
        context = self.context

        folder_path = '/'.join(context.getPhysicalPath())
        site = getSite()
        catalog = site.portal_catalog
        results = catalog.searchResults(
                  portal_type='abctune',
                  path={'query': folder_path, 'depth': 1},
                  )
        return results

    def getLocalFolders(self):
        context = self.context

        folder_path = '/'.join(context.getPhysicalPath())
        site = getSite()
        catalog = site.portal_catalog
        results = catalog.searchResults(
                  portal_type='Folder',
                  path={'query': folder_path, 'depth': 1},
                  )
        return results

    def getParent(self):
        context = self.context
        if context.portal_type == "Plone Site":
            return None
        else:
            return context.aq_parent
