# -*- coding: UTF-8 -*-
import logging
from zope.publisher.browser import BrowserView
from zope.component.hooks import getSite
from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')

class updateSubjects(BrowserView):
    """ AJAX method/view"""
    def __call__(self, subjects):
        logger.info(subjects)


class manageSubjects(BrowserView):

    def listSubjects(self):
        catalog = self.context.portal_catalog
        subjects = list(catalog.uniqueValuesFor('Subject'))
        logger.info(subjects)
        # import pdb;pdb.set_trace()
        logger.info(subjects.sort())
        return subjects
        
