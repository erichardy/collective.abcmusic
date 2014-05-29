#!/bin/sh

export PATH="/opt/eh/mypythontools/bin:$PATH"
PRODUCTNAME='collective.abcmusic'
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the templates.
i18ndude rebuild-pot --pot locales/${PRODUCTNAME}.pot --create ${I18NDOMAIN} .

# Synchronise the resulting .pot with the .po files
i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/*/LC_MESSAGES/${PRODUCTNAME}.po

I18NDOMAIN="plone"
i18ndude rebuild-pot --pot locales/${I18NDOMAIN}.pot --create ${I18NDOMAIN} .
i18ndude sync --pot locales/${I18NDOMAIN}.pot locales/*/LC_MESSAGES/${I18NDOMAIN}.po
