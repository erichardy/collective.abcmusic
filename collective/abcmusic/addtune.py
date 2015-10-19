from five import grok
from plone.directives import form

from zope import schema
from z3c.form import button
from plone.dexterity.browser import add

from Products.CMFCore.interfaces import ISiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from collective.abcmusic.abctune import IABCTune
from collective.abcmusic import _


class IAddTune(form.Schema):
    tuneType = schema.Set(title=_(u"Tune Type"),
                          value_type=schema.Choice(values=[_(u'Reel'),
                                                           _(u'Jig'),
                                                           _(u'Hornpipe')]
                                                   ),
                          )
    name = schema.TextLine(title=_(u"Your full name"))


class AddTune(add.DefaultAddForm):
    grok.name('add-tune')
    grok.require('zope2.View')
    grok.context(ISiteRoot)

    # change the schema below for a different addForm
    schema = IABCTune
    ignoreContext = True

    label = _(u"Add a new tune")
    description = _(u"Form used to add a new tune")

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)

        # call the base class version - this is very important!
        super(add.DefaultAddForm, self).update()

    @button.buttonAndHandler(_(u'Create the tune'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Redirect back to the front page with a status message

        IStatusMessage(self.request).addStatusMessage(_(u"Thank you"),
                                                      "info"
                                                      )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)

    @button.buttonAndHandler(_(u"Cancel the tune"))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)


class add_form(add.DefaultAddView):
    form = AddTune
