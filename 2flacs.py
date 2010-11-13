#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import locale

from glob import glob
from argparse import ArgumentParser

from lossless import getLossLessAudio, lossless_extensions
from util import infomsg, warnmsg, errormsg

_, default_encoding = locale.getdefaultlocale()

ext_cue_variants = [
                    '.cue',
                    '.CUE',
                    '.Cue',
                   ]

class NoChunkError(Exception):
    pass

def splitwrapper_both(chunk, cuefile):
    source = getLossLessAudio(chunk)
    source.split(cuefile)

def splitwrapper_only_chunk(chunk):
    cuefile = choosecuefile(chunk)
    splitwrapper_both(chunk, cuefile)

def splitwrapper_none():

    candicates = []

    for ext in lossless_extensions:
        pattern = u"*%s" % (ext)
        matches = glob(pattern)

        candicates.extend(matches)

    if not candicates :
        raise NoChunkError("no audio chunk is specifed/found!")

    # simple but working logic
    chunk = candicates[0]

    splitwrapper_only_chunk(chunk)


def comparebysize( file1, file2):

    size1 = os.stat(file1).st_size
    size2 = os.stat(file2).st_size

    if size1 < size2 :
        return -1
    elif size1 > size2:
        return 1
    else:
        return 0

def choosecuefile(chunk):

    basename, _ = os.path.splitext(chunk)

    candicates = [ ]

    for ext in ext_cue_variants:
        pattern = u"%s*%s" % (basename, ext)
        matches = glob(pattern)

        candicates += matches

    # globbing can't deal with filename containing '[,],*'
    if not candicates:

        basedir = os.path.dirname( os.path.realpath(chunk))

        # get all entries using ".cue" as extension
        entries = os.listdir(basedir)
        entries = [ entry for entry in entries if entry[-4:].lower() == ".cue" ]

        # prefer bigger cuefile, because it likely to contain more info
        entries.sort(comparebysize)
        candicates.extend(entries)

    bestchoice = candicates[0] if candicates else None

    return bestchoice


if __name__ == "__main__" :

    argparser = ArgumentParser(
                description="""split and convert one chunk of lossless
                            audio file into FLAC pieces """
                              )


    argparser.add_argument("-d", metavar="DIR", dest="dir",
                            help="the output position."
                          )

    argparser.add_argument("-f", metavar="FORMAT", dest="format",
                            help="the output audio format."
                          )

    argparser.add_argument("-g", metavar="REPLAYGAIN", dest="gain",
                            help="calculate replay-gain after splitting."
                          )

    argparser.add_argument("-n", metavar="NAMING", dest="naming",
                            help="scheme for naming output pieces."
                          )

    argparser.add_argument("chunk", metavar="CHUNK", nargs='?',
                            help="audio chunk to split and convert."
                          )

    argparser.add_argument("cuefile", metavar="CUEFILE",nargs='?',
                            help="audio chunk to split and convert."
                          )

    args  = argparser.parse_args()


    chunk   = args.chunk.decode(default_encoding) if args.chunk else u""
    cuefile = args.cuefile.decode(default_encoding) if args.cuefile else u""

    #try :
    if chunk and cuefile :
        splitwrapper_both(chunk, cuefile)
    elif chunk:
        splitwrapper_only_chunk(chunk)
    else:
        splitwrapper_none()
    #except Exception as e:
        #errormsg(e.message)



