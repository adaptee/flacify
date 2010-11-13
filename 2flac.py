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
    lossless = getLossLessAudio(source)

    lossless.convert(format)

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

