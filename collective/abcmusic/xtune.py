from five import grok
from zope import schema
from plone.namedfile.field import NamedImage
from plone.namedfile.field import NamedFile
from plone.directives import form

from collective.abcmusic import _

class IXtune(form.Schema):
    title = schema.TextLine(
            title=_(u"Tune name"),
        )
    description = schema.Text(
            title = _(u"Tune summary"),
            required = False,
        )
    form.primary('abc')
    abc = schema.Text(
            title = _(u"Tune abc"),
        )
    score = NamedImage (
            title = _("Score"),
            description = _('The score of the tune'),
            required = False,
        )
    midi = NamedFile (
            title = _("Midi"),
            description = _('Midi sound of the tune'),
            required = False,
        )
    mp3 = NamedFile (
            title = _("mp3"),
            description = _('The mp3 sound of the tune'),
            required = False,
        )