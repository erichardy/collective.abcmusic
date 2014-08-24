# -*- coding: UTF-8 -*-
import logging
from zope.publisher.browser import BrowserView
from zope.component.hooks import getSite
from zope.interface import Interface, implements
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope import schema

from plone.directives import form
from plone.supermodel import model
from z3c.form import field, button
from Products.CMFCore.interfaces import ISiteRoot
from five import grok

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from plone.formwidget.contenttree import PathSourceBinder
from plone.formwidget.contenttree import path_src_binder
from plone.formwidget.contenttree import ContentTreeFieldWidget
from plone.formwidget.contenttree import MultiContentTreeFieldWidget

from collective.plonefinder.widgets.referencewidget import FinderSelectFileWidget
from plone import api

logger = logging.getLogger('collective.abcmusic')


class IGetTunes(form.Schema):
    my_tunes = schema.Choice(title=u"Choice tunes",
                             description=u"Select one, please",
                             source="collective.abcmusic.getLocalTunes"
                           )
    """
    my_tunes = schema.List(title=u"Choice tunes",
                             description=u"Select one, please",
                             value_type=schema.Choice(
                               title=u"Selection",
                               vocabulary=u"collective.abcmusic.getLocalTunes"
                               )
                           )
    """

class getTunes(form.SchemaForm):
    grok.context(ISiteRoot)
    schema = IGetTunes
    ignoreContext = True

    def updateWidgets(self):
        super(getTunes, self).updateWidgets()
        self.fields['my_tunes'].widgetFactory = ReferenceBrowserWidget
        # self.fields['my_tunes'].widgetFactory = MultiContentTreeFieldWidget
        # self.widgets['my_tunes'].size = 20
        # import pdb;pdb.set_trace()
"""


class getTunes(BrowserView):

    def getLocalTunes(self):
        context = self.context

        folder_path = '/'.join(context.getPhysicalPath())
        site = getSite()
        catalog = site.portal_catalog
        results = catalog.searchResults(
                  portal_type='abctune',
                  path={'query': folder_path, 'depth': 1},
                  )
        return results

    def getLocalFolders(self):
        context = self.context

        folder_path = '/'.join(context.getPhysicalPath())
        site = getSite()
        catalog = site.portal_catalog
        results = catalog.searchResults(
                  portal_type='Folder',
                  path={'query': folder_path, 'depth': 1},
                  )
        return results

    def getParent(self):
        context = self.context
        if context.portal_type == "Plone Site":
            return None
        else:
            return context.aq_parent

    def js(self):
        script = u'<script type="text/javascript">'
        script += u'$(document).ready(function() {'
        script += u'$("div#get-tunes a.get-tunes-overlay").click(function(event){'
        script += u'event.preventDefault();'
        script += u'console.log(this.href) ;'
        script += u'$("div.pb-ajax").load(this.href + " #content");'
        script += u'});'
        script += u'});'
        script += u'</script>'
        return script

# gettunes_form_frame = wrap_form(getTunes, index=ViewPageTemplateFile("gettunes.pt"))

"""