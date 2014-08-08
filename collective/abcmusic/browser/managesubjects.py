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
        logger.info('updateSubjects: Subject List updated ' + str(l_subjects))
        return self.sujbectsStr()

    def sujbectsStr(self):
        subjects = self.context.subject
        subject_str = ''
        for s in subjects:
            subject_str += s + ', '
        return subject_str.strip(', ')

class manageSubjects(BrowserView):

    def listSubjects(self):
        catalog = self.context.portal_catalog
        subjects = list(catalog.uniqueValuesFor('Subject'))
        return subjects

    def currentSubjects(self):
        return list(self.context.subject)
