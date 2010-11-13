#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import locale

from glob import glob
from argparse import ArgumentParser

from lossless import getLossLessAudio, lossless_extensions
from util import infomsg, warnmsg, errormsg

_, default_encoding = locale.getdefaultlocale()

class NoChunkError(Exception):
    pass

def splitwrapper_both(chunk, cuefile):
    infomsg( "going to split audio trunk: %s" % chunk)
    source = getLossLessAudio(chunk)
    source.split(cuefile)

def splitwrapper_only_chunk(chunk):
    cuefile = choose_cuefile(chunk)
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


def filesize(f):
    return os.stat(f).st_size

def choose_cuefile(chunk):


    dirname = os.path.dirname( os.path.realpath(chunk) )
    entries = os.listdir( dirname)

    # all cuefiles under same folders
    cue_entries = [ entry for entry in entries if entry[-4:].lower() == ".cue" ]

    # all by file size, in descending order
    cue_entries.sort( key=filesize, reverse=True)

    # all cuefiles whose name contain chunk's name
    matching_entries = [ cue_entry for cue_entry in cue_entries if cue_entry.find(chunk) != -1   ]

    try :
        best_choice = matching_entries[0] if matching_entries else cue_entries[0]
    except IndexError:
        best_choice = None

    return best_choice

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

