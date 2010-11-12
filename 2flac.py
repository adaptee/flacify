#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import sys
import locale

from subprocess import call
from mutagen.flac import FLAC
from util import infomsg, check_audio_decodable, extensions
from lossless import APEFormat, FLACFormat, getLossLessFormat

_, default_encoding = locale.getdefaultlocale()

def conv2flac(source, target=None):

    source = unicode(source, default_encoding)

    # convert to .flac by default
    if not target:
        target = os.path.splitext(source)[0] + u".flac"

    check_audio_decodable(source)

    convert(source)

    copy_taginfo(source, target)

def convert(source):
    infomsg( "converting %s into FLAC format..." % source )

    command = [ 'shnconv','-o', 'flac', source ]
    code = call( command, shell=False)

def copy_taginfo( source, target ):

    source_format = getLossLessFormat(source)
    target_format = getLossLessFormat(target)

    taginfo = source_format.extract_taginfo()
    target_format.update_taginfo(**taginfo)

    return

if __name__ == "__main__" :

    if len(sys.argv) > 1 :
        sources = sys.argv[1:]

    for source in sources:
        conv2flac(source)
