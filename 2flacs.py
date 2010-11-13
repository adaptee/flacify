#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import locale

from glob import glob
from argparse import ArgumentParser
from subprocess import Popen, PIPE, call

from mutagen.flac import FLAC
from mutagen.apev2 import APEv2 as APE

from cuesheet.cueyacc import parsecuedata
from split import split
from util import infomsg, warnmsg, errormsg, extensions, parsecuefile

_, default_encoding = locale.getdefaultlocale()

class CuesheetNotFoundError(Exception):
    pass

class NoChunkError(Exception):
    pass

class MultiChunkError(Exception):
    pass

ext_cue_variants = [
                    '.cue',
                    '.CUE',
                    '.Cue',
                   ]


def get_embeded_cuesheet(chunk):

    _, ext = os.path.splitext(chunk)
    ext = ext.lower()

    if ext == '.flac':
        audio   = FLAC(chunk)
        cuedata = audio.get("cuesheet", "")[0]
        if cuedata :
            return parsecuedata(cuedata)
    elif ext == '.ape' :
        audio   = APE(chunk)
        cuedata = unicode( audio.get("cuesheet", "") )
        if cuedata :
            return parsecuedata(cuedata)
    elif ext == '.wv' :
        audio   = APE(chunk)
        cuedata = unicode( audio.get("cuesheet", "") )
        if cuedata :
            return parsecuedata(cuedata)
    elif ext == '.tta' :
        audio   = APE(chunk)
        cuedata = unicode( audio.get("cuesheet", "") )
        if cuedata :
            return parsecuedata(cuedata)


def splitwrapper_both(chunk, cuefile):

    cuesheet = parsecuefile(cuefile)
    split(chunk, cuesheet)


def splitwrapper_only_chunk(chunk):

    try :
        cuefile = pickcuefile(chunk)
        splitwrapper_both(chunk, cuefile)
    except CuesheetNotFoundError as e:
        warnmsg(e.message)

        infomsg("trying embeded cuesheet...")
        cuesheet = get_embeded_cuesheet(chunk)
        split(chunk, cuesheet)


def splitwrapper_only_cuefile(cuefile):

    infomsg("only cuefile")
    infomsg("cuefile:%s" % (cuefile) )

    chunk = pickchunk(cuefile)
    splitwrapper_both(chunk, cuefile)


def splitwrapper_none():

    chunk   = u""
    cuefile = u""

    for ext in extensions.keys():
        pattern = u"*%s" % (ext)
        matches = glob(pattern)

        if len(matches) > 1 :
            raise MultiChunkError(matches)
        elif len(matches) == 1:
            chunk = matches[0]
            break

    if not chunk :
        raise NoChunkError("no chunk is found!")

    splitwrapper_only_chunk(chunk)


def pickchunk(cuefile):

    chunk = u""

    basename,  _ = os.path.splitext(cuefile)

    candicates = map( lambda ext: basename + ext , extensions.keys())
    real_candicates = filter ( lambda path : os.path.exists(path), candicates)

    bestchoice = real_candicates[-1]
    #bestchoice = basename + u".ape"

    return bestchoice

def comparebysize( file1, file2):

    try:
        size1 = os.stat(file1).st_size
        size2 = os.stat(file2).st_size

        if size1 < size2 :
            return -1
        elif size1 > size2:
            return 1
        else:
            return 0
    except Exception as e:
        print (e)

def pickcuefile(chunk):

    basename, _ = os.path.splitext(chunk)

    candicates = [ ]

    for ext in ext_cue_variants:
        pattern = u"%s*%s" % (basename, ext)
        matches = glob(pattern)

        candicates += matches

    # globbing can't deal with filename containing '[,],*'
    if not candicates:

        # FIXME; a false assumption
        basedir = "."

        # get all entries using ".cue" as extension
        entries = os.listdir(basedir)
        entries = [ entry for entry in entries if entry[-4:].lower() == ".cue" ]

        # prefer bigger cuefile, because it likely to contain more info
        entries.sort(comparebysize)
        candicates.extend(entries)

    if not candicates :
        raise CuesheetNotFoundError("no suitable cuesheet is available")

    # stupid and naive logic ; but it works most of time.
    bestchoice = candicates[0]
    return bestchoice



def analyze_args(arg1, arg2 ):
    """
        which is for trunk, which is for cuefile
    """

    real_chunk   = u""
    real_cuefile = u""

    if arg1 and arg2 :
        real_chunk = arg1
        real_cuefile = arg2
    elif arg1:
        if ( arg1[-4:].lower() == u".cue" ):
            real_cuefile = arg1
        else:
            real_chunk = arg1
    else:
        pass

    return real_chunk, real_cuefile


if __name__ == "__main__" :

    argparser = ArgumentParser(
                description="""split and convert one chunk of lossless
                            audio file into FLAC pieces """
                           )

    argparser.add_argument("-c", metavar="CODEC", dest="codec",
                            help="the output codec."
                          )

    argparser.add_argument("-e", metavar="ENCODING", dest="encoding",
                            help="the encoding of cuesheet."
                          )

    argparser.add_argument("-d", metavar="DIR", dest="dir",
                            help="the output position."
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

    chunk, cuefile = analyze_args( chunk, cuefile)

    #try :
    if chunk and cuefile :
        splitwrapper_both(chunk, cuefile)
    elif chunk:
        splitwrapper_only_chunk(chunk)
    elif cuefile:
        splitwrapper_only_cuefile(cuefile)
    else:
        splitwrapper_none()
    #except Exception as e:
        #errormsg(e.message)



