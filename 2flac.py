#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import sys

from subprocess import PIPE, call
from util import infomsg, supported_exts, ext2decoder

def conv2flac(target):

    target = unicode(target)

    basename, ext = os.path.splitext(target)
    ext = ext.lower()

    if ext == ".flac" :
        infomsg( "%s is already in flac format." % (target) )
    elif ext in supported_exts:
        convert(target)
    else:
        infomsg( "%s has a un-supported format." % (target) )

def convert(target):

    command = [ 'shnconv','-o', 'flac', target ]
    code = call( command, shell=False, stdin=PIPE, stdout=PIPE)

def copy_taginfo( src, dest ):
    pass


if __name__ == "__main__" :

    if len(sys.argv) > 1 :
        targets = sys.argv[1:]

    for target in targets:
        conv2flac(target)

