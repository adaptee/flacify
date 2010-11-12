#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import locale

import subprocess
from argparse import ArgumentParser

from lossless import getLossLessAudio
from util import infomsg, check_audio_decodable

_, default_encoding = locale.getdefaultlocale()

def toAnotherForamt(source, format="flac" ):

    source = unicode(source, default_encoding)

    check_audio_decodable(source)

    target = convert(source, format)

    copy_taginfo(source, target)

def convert(source, format="flac" ):

    command = [ 'shntool', 'conv', '-o', format, source ]
    code = subprocess.call( command, shell=False)

    target = os.path.splitext(source)[0] + "." + format
    return target

def copy_taginfo( source, target ):

    source = getLossLessAudio(source)
    target = getLossLessAudio(target)

    taginfo = source.extract_taginfo()
    target.update_taginfo(**taginfo)

if __name__ == "__main__" :

    argparser = ArgumentParser(
                            description=
                            """convert lossless audio files into another lossless codec. """
                              )

    argparser.add_argument( "-f",
                            metavar="FORMAT",
                            dest="format",
                            default="flac",
                            choices=['flac', 'ape', 'tta', 'wv', 'wavpack', 'wav' ],
                            help="target format. valid values are flac, ape, tta, wavpack and wav."
                          )

    argparser.add_argument( "files",
                            metavar="FILE",
                            nargs='+',
                            help="lossless audio file to convert."
                          )

    args    = argparser.parse_args()

    sources = args.files
    format  = args.format.lower()

    # normalize alias
    if format == 'wavpack':
        format = 'wv'

    for source in sources:
        toAnotherForamt(source, format)

