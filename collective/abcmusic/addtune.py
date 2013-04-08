from five import grok
from plone.directives import form

from zope import schema
from z3c.form import button

from Products.CMFCore.interfaces import ISiteRoot
from Products.statusmessages.interfaces import IStatusMessage

from collective.abcmusic import _

class IAddTune(form.Schema):
    tuneType = schema.Set (
        title = _(u"Tune Type"),
        value_type=schema.Choice(values=[_(u'Reel'), _(u'Jig'), _(u'Hornpipe')]),
        )
    name = schema.TextLine(
            title=_(u"Your full name"),
        )

class AddTune(form.SchemaForm):
    grok.name('add-tune')
    grok.require('zope2.View')
    grok.context(ISiteRoot)
    
    schema = IAddTune
    ignoreContext = True
    
    label = _(u"Add a new tune")
    description = _(u"Form used to add a new tune")
    
    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)
        
        # call the base class version - this is very important!
        super(AddTune, self).update()
    
    @button.buttonAndHandler(_(u'Create'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        
        # Redirect back to the front page with a status message

        IStatusMessage(self.request).addStatusMessage(
                _(u"Thank you for your order. We will contact you shortly"), 
                "info"
            )
        
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
        
    @button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
