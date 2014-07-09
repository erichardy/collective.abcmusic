# usefull documentations :
# http://developer.plone.org/forms/z3c.form.html
# http://developer.plone.org/forms/files.html
# http://pythonhosted.org/z3c.form/

import logging
from five import grok
from plone.directives import form
from z3c.form import button
from Products.CMFCore.interfaces import ISiteRoot
from plone.namedfile.field import NamedFile
from zope.component import getUtility

from plone.i18n.normalizer.interfaces import INormalizer

from collective.abcmusic.utils import removeNonAscii
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
                tuneId = normalizer.normalize(title, locale='fr')
                ## logger.info("getTuneId:" + tuneLine + ':' + tuneId)
                idOrigine = tuneId
                i = 1
                while tuneId in context.keys():
                    tuneId = idOrigine + '-' + str(i).zfill(3)
                    i += 1
                return tuneId
        return 'collective.abcmusic.NoId'

    def getTuneTitle(self, tune):
        """returns a title  from the title tune"""
        for tuneLine in tune:
            if tuneLine[:2] == 'T:':
                title = tuneLine.split(':')[1]
                return title
        return 'collective.abcmusic.NoTitle'

    def createTune(self, newtune=None, tuneId=None, tuneTitle=None):
        self.context.invokeFactory(type_name='abctune',
                                   id=tuneId,
                                   abc=newtune,
                                   title=tuneTitle)
        ## logger.info('createTune:' + tuneId)
        # tune = self.context[tuneId]
        # tune.abc = newtune
        # return tune

    def processABC(self, data):
        # tunes = data.split('\n')
        data = removeNonAscii(data)
        rawtunes = data.split('X:')
        for rawtune in rawtunes:
            tune = rawtune.split('\n')[1:]
            tune.insert(0, 'X:1')
            newtune = ('\n').join(tune)
            tuneId = self.getTuneId(tune)
            tuneTitle = self.getTuneTitle(tune)
            if tuneId != 'collective.abcmusic.NoId':
                self.createTune(newtune=newtune,
                                tuneId=tuneId,
                                tuneTitle=tuneTitle)
        # import pdb;pdb.set_trace()

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        tune = data["abc_file"].data
        self.processABC(tune)
        self.status = "Thank you very much!"

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
