# -*- coding: UTF-8 -*-
from collective.z3cform.widgets.token_input_widget import TokenInputFieldWidget
from collective.z3cform.widgets.enhancedtextlines import EnhancedTextLinesFieldWidget
from plone.app.dexterity.behaviors.metadata import ICategorization
from plone.app.z3cform.interfaces import IPloneFormLayer
from z3c.form.interfaces import IFieldWidget
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer


"""
Need to de-activate the js resource :
++resource++collective.z3cform.widgets/related.js
-> incompatible with js fonctionalities in abcmusic-tuneViews.js (???)
"""

@adapter(getSpecification(ICategorization['subjects']), IPloneFormLayer)
@implementer(IFieldWidget)
def SubjectsFieldWidget(field, request):
    widget = FieldWidget(field, TokenInputFieldWidget(field, request))
    return widget

