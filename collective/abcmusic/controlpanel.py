from plone.directives import form
from zope import schema
from plone.app.registry.browser import controlpanel

from collective.abcmusic import _

class IABCMusicSettingsForm(form.Schema):
    templates = schema.Text(
                            title = _(u"templates"),
                            description = _(u"abcmusic templates description"),
                            )

class ABCMusicSettingsForm(controlpanel.RegistryEditForm):
    schema = IABCMusicSettingsForm
    label = _(u"ABC Music Settings")
    description = _(u"ABCMusicSettingsDescription")
    
    def updateFields(self):
        super(ABCMusicSettingsForm , self).updateFields()

    def updateWidgets(self):
        super(ABCMusicSettingsForm , self).updateWidgets()

class ABCMusicSettingsFormSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ABCMusicSettingsForm

