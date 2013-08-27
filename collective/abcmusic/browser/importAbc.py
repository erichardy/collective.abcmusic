import logging
from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from AccessControl import getSecurityManager
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')

class importAbc(BrowserView):
    def __call__(self):
        return 'dans importAbc'