#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from glob import glob
from util import parsecuefile

cuefiles  = glob("cuesheet/test/@cue/*.cue")

#print cuefiles

for cuefile in cuefiles :
    cuesheet = parsecuefile( cuefile)
    print ("#OK with : %s" % (cuefile))
    print cuesheet.debug_repr()

