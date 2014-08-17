# -*- coding: utf8 -*-
import logging
from Products.CMFCore.utils import getToolByName
PROFILE = 'profile-collective.abcmusic:default'

# TODO : new upgrade
# convert all keywords which are not unicode to unicode
# change the coding of the keywords management : only manipulate unicode
# http://sametmax.com/lencoding-en-python-une-bonne-fois-pour-toute/
# http://www.joelonsoftware.com/articles/Unicode.html
# ch = 'chaîne' # type str
# uch = ch.decode('utf8') # type unicode


def common(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILE)


def setTuneKeys(context, logger=None):
    if logger is None:
        logger = logging.getLogger('collective.abcmusic')
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE, 'catalog')
    catalog = getToolByName(context, 'portal_catalog')
    # thanks to http://maurits.vanrees.org/weblog/archive/2009/12/catalog
    # first add index to catalog
    indexes = catalog.indexes()
    indexables = []
    if 'keys' in indexes:
        catalog.delIndex('keys')
    if not 'tunekeys' in indexes:
        catalog.addIndex('tunekeys', 'KeywordIndex')
        indexables.append('tunekeys')
        logger.info("Added %s for field %s.", 'KeywordIndex', 'keys')
    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)
    #
    brains = catalog(portal_type='abctune')
    nbtunes = 0
    nbkeys = 0
    for brain in brains:
        tune = brain.getObject()
        abc = tune.abc
        tune.tunekeys = []
        for line in abc.split('\n'):
            if line[:2] == 'K:':
                key = line.split(':')[1].strip()
                tune.tunekeys.append(key)
                # logger.info(tune.title + '/' + str(tune.keys))
                # logger.info(key)
                tune.reindexObject()
                nbkeys += 1
        nbtunes += 1
    setup.runImportStepFromProfile(PROFILE, 'catalog')
    logger.info("%s tunes, %s keys added." % (nbtunes, nbkeys))


def setNewKeys(context, logger=None):
    """new field added : keys
    """
    if logger is None:
        logger = logging.getLogger('collective.abcmusic')
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE, 'catalog')
    catalog = getToolByName(context, 'portal_catalog')
    # thanks to http://maurits.vanrees.org/weblog/archive/2009/12/catalog
    # first add index to catalog
    indexes = catalog.indexes()
    indexables = []
    if not 'keys' in indexes:
        catalog.addIndex('keys', 'KeywordIndex')
        indexables.append('keys')
        logger.info("Added %s for field %s.", 'KeywordIndex', 'keys')
    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)
    #

    brains = catalog(portal_type='abctune')
    nbtunes = 0
    nbkeys = 0
    """
    # we do nothing because the field 'tunekeys' replace 'keys'
    for brain in brains:
        tune = brain.getObject()
        abc = tune.abc
        tune.keys = []
        for line in abc.split('\n'):
            if line[:2] == 'K:':
                key = line.split(':')[1].strip()
                tune.keys.append(key)
                # logger.info(tune.title + '/' + str(tune.keys))
                # logger.info(key)
                tune.reindexObject()
                nbkeys += 1
        nbtunes += 1
    """
    setup.runImportStepFromProfile(PROFILE, 'catalog')
    logger.info("%s tunes, %s keys added." % (nbtunes, nbkeys))
