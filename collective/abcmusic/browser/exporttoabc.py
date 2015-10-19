# usefull documentations :
# http://kevinharvey.net/2011/02/28/create-and-download-a-csv-or-any-other-file-type-with-a-plone-view/

import logging
from zope.publisher.browser import BrowserView
from zope.component.hooks import getSite
# from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')


class exportToAbc(BrowserView):

    def __call__(self):
        context = self.context
        folder_path = '/'.join(context.getPhysicalPath())
        site = getSite()
        filename = context.getId() + '.abc'
        catalog = site.portal_catalog
        results = catalog.searchResults(portal_type='abctune',
                                        path={'query': folder_path,
                                              'depth': 1},
                                        )
        abcFile = ''

        for tunes in results:
            tune = tunes.getObject()
            abc = tune.abc
            for line in abc.split('\n'):
                abcFile += line + '\n'
                if line[:2] == 'X:':
                    subjects = tune.subject
                    if len(subjects) > 0:
                        for subject in subjects:
                            abcFile += '%ABCKeyWord:' + subject + '\n'
                            logger.info(subject)
            abcFile += '\n\n'
        self.request.response.setHeader('Content-Type', 'text/abc')
        self.request.response.setHeader('Content-Disposition',
                                        'attachment; filename="%s"' % filename)
        return abcFile
