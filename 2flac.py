#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import sys

from subprocess import call
from util import infomsg, check_audio_decodable

def conv2flac(target):

    target = unicode(target, "utf8")
    check_audio_decodable(target)

    convert(target)

def convert(target):

    command = [ 'shnconv','-o', 'flac', target ]
    code = call( command, shell=False)

def copy_taginfo( src, dest ):
    pass

if __name__ == "__main__" :

    if len(sys.argv) > 1 :
        targets = sys.argv[1:]

    for target in targets:
        conv2flac(target)
