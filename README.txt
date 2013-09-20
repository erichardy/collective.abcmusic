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

At the starting point of this project (Dec. 2012), two ways are explored :
- interface between dexterity content types and command line tools : abcm2ps (or abc2ps) and abcMIDI
- use of abcjs javascripts. See module collective.js.abcjs on github.

See web sites for more informations :
* abcm2ps : http://moinejf.free.fr/
* abcMIDI : http://abc.sourceforge.net/abcMIDI/
* abcjs : http://code.google.com/p/abcjs/

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

This module is tested for plone 4.2.x. So, be aware of versions to specify in buildout.cfg :
collective.js.abcjs==1.4.6
collective.js.jqueryui==1.8.16.9

Not yet tested on plone 4.3

TOTO
====
* make a method to manage png image accordingly with the real size the tune
  (should use eps transformation...)
* add automaticaly a field Q: if it doesn't exist
* manage permissions... 