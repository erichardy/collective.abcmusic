# -*- coding: UTF-8 -*-
import logging
from plone.directives import form
# from plone.supermodel import model
# from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from zope import schema
# from plone.directives import form
# from plone.supermodel import model
from z3c.form import field
from Products.CMFCore.interfaces import ISiteRoot
from five import grok

from collective.plonefinder.widgets.referencewidget import FinderSelectWidget
from collective.plonefinder.widgets.referencewidget import FinderSelectFileWidget
from plone import api

from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')


class FinderSelectTuneWidget(FinderSelectWidget):
    finderlabel = _(u'Browse for files')
    types = ['abctune']
    allowupload = 0
    allowaddfolder = 0


class IGetTunes(form.Schema):

    # form.widget(my_tunes='collective.abcmusic.browser.gettunes.\
    # FinderSelectTuneWidget')
    form.widget(my_tunes=FinderSelectFileWidget)
    my_tunes = schema.Tuple(title=u"Choice tunes",
                            description=u"Select one, please",
                            default=()
                            )


class getTunes(form.SchemaForm):
    grok.context(ISiteRoot)
    schema = IGetTunes
    # fields = field.Fields(IGetTunes)
    # fields['my_tunes'].widgetFactory = FinderSelectTuneWidget
    ignoreContext = True
    # fields = field.Fields(IGetTunes)
    # fields["my_tunes"].widgetFactory = FinderSelectTuneWidget
    label = u"Choose a tune..."
    description = u"Form to choose a tune"

    def updateWidgets(self):
        super(getTunes, self).updateWidgets()
        fields = field.Fields(IGetTunes)
        fields['my_tunes'].widgetFactory = FinderSelectFileWidget
        # self.fields['my_tunes'].widgetFactory = FinderSelectTuneWidget
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
        script += u'$("div#get-tunes a.get-tunes-overlay").'
        script += 'click(function(event){'
        script += u'event.preventDefault();'
        script += u'console.log(this.href) ;'
        script += u'$("div.pb-ajax").load(this.href + " #content");'
        script += u'});'
        script += u'});'
        script += u'</script>'
        return script

# gettunes_form_frame = wrap_form(getTunes,
                                  index=ViewPageTemplateFile("gettunes.pt")
                                  )

"""
