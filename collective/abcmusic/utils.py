# -*- coding: utf-8 -*-
from zope.component.hooks import getSite
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from five import grok

def removeNonAscii(s):
    return "".join(i for i in s if ord(i) < 128)


class _getLocalTunes(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        folder_path = '/'.join(context.getPhysicalPath())
        site = getSite()
        catalog = site.portal_catalog
        results = catalog.searchResults(
                  portal_type='abctune',
                  path={'query': folder_path, 'depth': 1},
                  )
        terms = []
        i = 0
        for tunes in results:
            tune = tunes.getObject()
            value = str(i)
            token = str(i)
            label = tune.title
            terms.append(SimpleVocabulary.createTerm(value,
                                                 str(token),
                                                 label))
            i += 1

        return SimpleVocabulary(terms)

getLocalTunes = _getLocalTunes()
# grok.global_utility(_getLocalTunes, name=u"collective.abcmusic.getLocalTunes")
