import logging
from zope.publisher.browser import BrowserView

class onlyABC(BrowserView):
    def getABC(self):
        try:
            return self.context.abc
        except:
            return u'no-abc'
