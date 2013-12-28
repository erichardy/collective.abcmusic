import logging
from plone.app.portlets.portlets import base
from zope import schema
from zope.interface import implements
from zope.formlib import form

from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.portlets.interfaces import IPortletDataProvider
from collective.abcmusic import _
logger = logging.getLogger('collective.abcmusic')

class ITunesListingPortlet(IPortletDataProvider):
    count = schema.Int(title=_(u'size of the box'),
                       description=_(u'Maximum size of the box.'),
                       required=True,
                       default=20)

class Assignment(base.Assignment):
    implements(ITunesListingPortlet)

    def __init__(self, count=5):
        self.count = count

    @property
    def title(self):
        return _(u"abctunes listing")

class AddForm(base.AddForm):
    form_fields = form.Fields(ITunesListingPortlet)
    label = _(u"Add Tunes listing Portlet")
    description = _(u"This portlet the tunes in the current folder.")

    def create(self, data):
        return Assignment(count=data.get('count', 20))

class EditForm(base.EditForm):
    form_fields = form.Fields(ITunesListingPortlet)
    label = _(u"Edit Tunes listing Portlet")
    description = _(u"This portlet the tunes in the current folder.")

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('tuneslisting.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self.anonymous = portal_state.anonymous()  # whether or not the current user is Anonymous
        self.portal_url = portal_state.portal_url()  # the URL of the portal object

        # a list of portal types considered "end user" types
        self.typesToShow = portal_state.friendly_types()

        plone_tools = getMultiAdapter((context, self.request), name=u'plone_tools')
        self.catalog = context.portal_catalog

    def render(self):
        return self._template()

    @property
    def available(self):
        """Show the portlet only if there are one or more elements."""
        # return not self.anonymous and len(self._data())
        return True

    def portlet_size(self):
        count = self.data.count
        nb_results = len(self._data())
        if nb_results < count:
            return nb_results
        else:
            return count
                          
        
    def tunes_items(self):
        return self._data()

    def tunes_link(self):
        return '%s/tune' % self.portal_url

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        # logger.info(context)
        # logger.info(context.aq_parent)
        if context.portal_type == 'Folder':
            folder_path = '/'.join(context.getPhysicalPath())
        else:
            folder_path = '/'.join(context.aq_parent.getPhysicalPath())
        results = self.catalog(
                       Type = "abctune",
                       path={'query': folder_path, 'depth': 1})
        return results
