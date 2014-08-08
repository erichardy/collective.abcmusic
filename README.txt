Introduction
============

This is an add-on for plone.

This project was born from :
1- I play Irish music
2- I use intensively abc music notation for training and organizing my sets of tunes
3- I develop some plone add-ons at my job

The goal is to use plone to store tunes and friendly manipulate them.

ABC music notation is the heart of this project.
One of the main web site related to abc is : http://abcnotation.com/  

See web sites for more informations :
* abcm2ps : http://moinejf.free.fr/
* abcMIDI : http://abc.sourceforge.net/abcMIDI/
* abcjs : http://code.google.com/p/abcjs/

Note about QuickTime : in recent QuickTime versions, Apple removed MIDI support.
So, may be it is possible to recover MIDI support from older versions.
see : http://support.apple.com/kb/DL923

DEPENDENCIES
============
* abcm2ps
* abc2midi
* convert (ImageMagick package)
* ps2pdf (ubuntu : ghostscript package)
* lame


NOTE
====
If you want to listen midi inline, it is necessary to use an old version of Quicktime(R)
which can be downloaded from : http://support.apple.com/kb/DL923 

Bug
===
a bug like this sometimes appears (but not always) :
'_DummyThread' object has no attribute '_Thread__block'",) in <module 'threading'
See comments at :
http://stackoverflow.com/questions/13193278/understand-python-threading-bug
code to be added :
    # import threading
    # threading._DummyThread._Thread__stop = lambda x: 42

Install
=======
This module is not yet on pypi, so use mr.developer to check it out from github.

Currently dev for Plone 4.3.x

For quicktime(R) versions, see : http://support.apple.com/downloads/#quicktime

Features
========

A dexterity content type is defined so it can be added in a folder.

TODO
====
* DONE / fix modification time when tune is modified by standard view (not by "edit" menu)
* DONE / when manage keywords, only display keywords of owned abctunes
* export tune or tunes as zipfile
* get command lines for abc -> ps, ps -> jpeg, abc->midi, midi->mp3 from controlpanel
* when export a folder to a file, save also keywords in abc file as tagged comments and manage them in import
* new content type : tune repository with custom views
* tuneset : add tune by selection from directory browser
* manage better switching with MidiJS view
* overlaies for help and explanations
* keyboard bindings : i.e. to start play with a key pressed
* choose to create MP3 when a tune is created, also for batch import of abc file containing many tunes
* create indexes in the catalog for use with collections (catalog.xml and registry.xml). Now only TuneTypes.
* add CSS for standard addForm
* manage O: field in multiple tunes at once in a folder (for example : add O: field)
* create a public database of tunes from which a tune can be added to a owned folder
  ...perhaps by a specific add form (?)
* improve the IHM : which kind of menus?
