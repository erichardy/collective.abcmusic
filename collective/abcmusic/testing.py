"""
from plone.testing import z2

from plone.app.testing import *
import collective.abcmusic

FIXTURE = PloneWithPackageLayer(zcml_filename="configure.zcml",
                                zcml_package=collective.abcmusic,
                                additional_z2_products=[],
                                gs_profile_id='collective.abcmusic:default',
                                name="collective.abcmusic:FIXTURE")

INTEGRATION = IntegrationTesting(bases=(FIXTURE,),
                        name="collective.abcmusic:Integration")

FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,),
                        name="collective.abcmusic:Functional")
"""
