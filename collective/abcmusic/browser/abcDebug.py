from zope.publisher.browser import BrowserView
import logging
from plone import api



class abcDebug(BrowserView):
    def __call__(self):
        context = self.context
        import pdb;pdb.set_trace()