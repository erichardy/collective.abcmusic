# -*- coding: UTF-8 -*-
import logging
from zope.publisher.browser import BrowserView
from plone import api
logger = logging.getLogger('collective.abcmusic')


class updateSubjects(BrowserView):
    """ AJAX method/view"""
    def __call__(self, subjects):
        # NB: javascript allways returns str strings (not utf8)
        # keywords must be converted to utf8 before to be set to the object !!
        # logger.info(self.context)
        context = self.context
        # because context may be a view...
        try:
            tune = context.portal_type
        except:
            tune = context.context.portal_type
            context = self.context.context
        # import pdb;pdb.set_trace()
        l_subjects = [self.to_unicode(subject)
                      for subject in subjects.strip('|').split('|')
                      if subject]
        # import pdb;pdb.set_trace()
        context.subject = list(l_subjects)
        context.reindexObject(idxs=["subject"])
        # logger.info('updateSubjects: Subject List updated ' + str(l_subjects))
        return self.sujbectsString(context)

    def sujbectsString(self, context):
        subjects = context.subject
        subject_str = ''
        for s in subjects:
            subject_str += s + ', '
        return subject_str.strip(', ')

    def to_unicode(self, s):
        return s.decode('utf-8') if isinstance(s, str) else s

class manageSubjects(BrowserView):

    def listSubjects(self):
        catalog = self.context.portal_catalog
        subjects = list(catalog.uniqueValuesFor('Subject'))
        return subjects

    def listOwnedSubjects(self):
        current_user = api.user.get_current()
        catalog = self.context.portal_catalog
        abctunes = catalog(portal_type='abctune', owner=current_user)
        subjects = []
        for abctune in abctunes:
            keywords = list(abctune.getObject().subject)
            # logger.info(keywords)
            for k in keywords:
                if not k in subjects:
                    subjects.append(k)
        # sorting will be possible when all keywords in same encoding : utf8 !
        subjects.sort()
        # logger.info(subjects)
        return subjects

    def currentSubjects(self):
        return list(self.context.subject)
