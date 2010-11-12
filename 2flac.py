#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import sys
import locale

from subprocess import call
from mutagen.flac import FLAC
from util import infomsg, check_audio_decodable, extensions

_, default_encoding = locale.getdefaultlocale()

def conv2flac(source):

    source = unicode(source, default_encoding)
    target = os.path.splitext(source)[0] + u".flac"

    check_audio_decodable(source)

    convert(source)

    copy_taginfo(source, target)

def convert(source):

    command = [ 'shnconv','-o', 'flac', source ]
    code = call( command, shell=False)

def copy_taginfo( src, dest ):

    _, ext = os.path.splitext(src)

    tagextracter = extensions[ext]["tagextracter"]

    taginfo = tagextracter(src)

    flac = FLAC(dest)

    for key in taginfo.keys():
        flac[key] = taginfo[key]

    flac.save()


if __name__ == "__main__" :

    if len(sys.argv) > 1 :
        sources = sys.argv[1:]

    for source in sources:
        conv2flac(source)
