# usefull documentations :
# http://developer.plone.org/forms/z3c.form.html
# http://developer.plone.org/forms/files.html
# http://pythonhosted.org/z3c.form/

import logging
from five import grok
from plone.directives import form

from zope import schema
from z3c.form import button

from Products.CMFCore.interfaces import ISiteRoot
from Products.statusmessages.interfaces import IStatusMessage

from plone.namedfile.field import NamedFile
from plone.i18n.normalizer import idnormalizer

from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from AccessControl import getSecurityManager
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.abcmusic import _

logger = logging.getLogger('collective.abcmusic')

class IImportABC(form.Schema):
    abc_file = NamedFile(
            title=_(u"import a file containing one or more abc tunes"),
        )

class importAbc(form.SchemaForm):
    grok.name('importABC')
    grok.require('zope2.View')
    grok.context(ISiteRoot)
    
    schema = IImportABC
    ignoreContext = True
    
    label = _(u"import abc file")
    description = _(u"This will create abctune(s)")
    
    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Do something with valid data here

        # Set status on this form page
        # (this status message is not bind to the session and does not go thru redirects)
        self.status = "Thank you very much!"

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """