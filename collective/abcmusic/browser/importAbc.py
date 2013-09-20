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
from plone.i18n.normalizer.interfaces import INormalizer
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
    
    def getTuneId(self, tune):
        """returns an Id from the title tune"""
        context = self.context
        normalizer = getUtility(INormalizer)
        for tuneLine in tune:
            if tuneLine[:2] == 'T:':
                title = tuneLine.split(':')[1]
                id = normalizer.normalize(title, locale = 'fr')
                logger.info("getTuneId:" + tuneLine + ':' + id)
                idOrigine = id
                i = 1
                while id in context.keys():
                    id = idOrigine + '-' + str(i).zfill(3)
                    i += 1
                return id
        return 'collective.abctune.NoId'

    def getTuneTitle(self, tune):
        """returns a title  from the title tune"""
        for tuneLine in tune:
            if tuneLine[:2] == 'T:':
                title = tuneLine.split(':')[1]
                return title
        return 'collective.abctune.NoTitle'
        
    def createTune(self, newtune=None, tuneId=None, tuneTitle=None):
        self.context.invokeFactory(type_name='abctune' , id=tuneId, abc=newtune,title=tuneTitle)
        logger.info('createTune:' + tuneId)
        # tune = self.context[tuneId]
        # tune.abc = newtune
        # return tune

    def removeNonAscii(self,s): return "".join(i for i in s if ord(i)<128)
    
    def processABC(self , data):
        # tunes = data.split('\n')
        data = self.removeNonAscii(data)
        rawtunes = data.split('X:')
        for rawtune in rawtunes:
            tune = rawtune.split('\n')[1:]
            tune.insert(0 ,'X:1')
            newtune = ('\n').join(tune)
            tuneId = self.getTuneId(tune)
            tuneTitle = self.getTuneTitle(tune)
            if tuneId != 'collective.abctune.NoId':
                self.createTune(newtune=newtune, tuneId=tuneId , tuneTitle=tuneTitle)  
        # import pdb;pdb.set_trace()
    
    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Do something with valid data here
        tune = data["abc_file"].data
        self.processABC(tune)
        # Set status on this form page
        # (this status message is not bind to the session and does not go thru redirects)
        self.status = "Thank you very much!"

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """