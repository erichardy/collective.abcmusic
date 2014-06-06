# -*- coding: UTF-8 -*-
import logging
from zope.publisher.browser import BrowserView

logger = logging.getLogger('collective.abcmusic')

class updateSubjects(BrowserView):
    """ AJAX method/view"""
    def __call__(self, subjects):
        l_subjects = [subject 
                      for subject in subjects.strip('|').split('|')
                      if subject]
        self.context.subject = list(l_subjects)
        self.context.reindexObject(idxs=["subject"])
        return 'ok'


class manageSubjects(BrowserView):

    def listSubjects(self):
        catalog = self.context.portal_catalog
        subjects = list(catalog.uniqueValuesFor('Subject'))
        return subjects
        
    def currentSubjects(self):
        return list(self.context.subject)