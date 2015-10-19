from zope.publisher.browser import BrowserView


class abcDebug(BrowserView):
    def __call__(self):
        import pdb
        pdb.set_trace()
