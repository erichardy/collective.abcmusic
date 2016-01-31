# -*- coding: utf-8 -*-

from plone.directives import form
from zope import schema
from plone.app.registry.browser import controlpanel

from collective.abcmusic import _

templates_desc = u"abcmusic templates description"
public_tunes_desc = u"relative to the root plone site"
group_quotas_desc = u"one line per group, in the format : groupName:maxItems"


class IABCMusicSettingsForm(form.Schema):
    templates = schema.Text(title=_(u"templates"),
                            description=_(templates_desc),
                            required=False,
                            )
    public_tunes = schema.TextLine(title=_(u"Path to the public tune base"),
                                   description=_(public_tunes_desc),
                                   required=False,
                                   )
    group_quotas = schema.Text(title=_(u"quota for group members (max items)"),
                               description=_(group_quotas_desc),
                               required=False,
                               )


class ABCMusicSettingsForm(controlpanel.RegistryEditForm):
    schema = IABCMusicSettingsForm
    label = _(u"ABC Music Settings")
    description = _(u"ABCMusicSettingsDescription")

    def updateFields(self):
        super(ABCMusicSettingsForm, self).updateFields()

    def updateWidgets(self):
        super(ABCMusicSettingsForm, self).updateWidgets()


class ABCMusicSettingsFormControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ABCMusicSettingsForm
