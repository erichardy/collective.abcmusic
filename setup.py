from setuptools import setup, find_packages
import os

version = '0.4'
long_description = open("README.txt").read()
long_description += "\n" + open(os.path.join("docs",
                                             "HISTORY.txt")).read()

setup(name='collective.abcmusic',
      version=version,
      description="Addon for Plone",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=["Programming Language :: Python",
                   "Framework :: Plone",
                   "Framework :: Plone :: 4.2",
                   "Framework :: Plone :: 4.3",
                   ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'plone.api',
          'five.grok',
          'plone.app.z3cform',
          'plone.directives.dexterity',
          'plone.directives.form',
          'plone.app.dexterity',
          'collective.dexteritytextindexer',
          'plone.namedfile[blobs]',
          'plone.formwidget.namedfile',
          'collective.autopermission',
          'plone.formwidget.contenttree',
          'collective.plonefinder',
          'collective.js.jqueryui',
          'collective.js.abcjs==1.10',
          # -*- Extra requirements: -*-
      ],
      extras_require=dict(
          tests=['plone.app.testing'],
      ),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
