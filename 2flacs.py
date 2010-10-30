#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
from glob import glob
from argparse import ArgumentParser

import chardet
from cueyacc import parsecuefile
from split import split

ext2decoder    = {
                    ".ape"  : "mac",
                    ".flac" : "flac",
                    ".tta"  : "ttaenc",
                    ".wv"   : "wvunpack",
                 }

decoder_checking             = { }
decoder_checking["mac"]      = "please install mac"
decoder_checking["flac"]     = "please install flac"
decoder_checking["wvunpack"] = "please install wavpack"
decoder_checking["ttaenc"]   = "please install ttaenc"


def splitwrapper_both(chunk, cuefile):
    pass

def splitwrapper_only_chunk(chunk):

    basename, ext = os.path.splitext(chunk)
    ext = ext.lower()

    decoder = ext2decoder.get(ext)

    if not decoder :
        raise ValueError( " %s is not supported" % (ext) )

    try :
        checkdecoder( decoder, decoder_checking[decoder] )

    except Exception as e :
        print (e)
        return

    print ("analyazing cuesheet...")
    cuefile = pickcuefile(chunk)
    cuesheet = parsecuefile(cuefile)

    split(chunk, cuesheet)

def splitwrapper_only_cuefile(cuefile):
    pass

def splitwrapper_none():
    pass

def checkdecoder( decoder, error_msg):

    command = "which %s &> /dev/null" % (decoder)
    code  = os.system(command)

    # decoder not availabe in $PATH
    if code != 0:
        raise ValueError(error_msg)

def pickcuefile(chunk):

    basename, extenseion = os.path.splitext(chunk)

    candicates = glob( ( "%s*.cue" % basename) )

    # FIXME
    # navie logic
    bestchoice =  basename + ".cue"

    # FIXME
    # rude checking
    #assert decodable(bestchoice)

    return bestchoice

def decodable(cuefile):
    """
       Does cuefile use supported encodings?
    """
    supported_encodings = [ 'ascii',
                            'utf-8', 'utf16-le',
                            'cp936', 'gb18030',
                            'sjis',
                          ]

    guess = chardet.detect(cuefile)
    encoding   = guess['encoding']
    confidence = guess['confidence']

    if encoding in supported_encodings and confidence > 0.98 :
        return True
    else:
        return False

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

    argparser.add_argument("chunk", metavar="CHUNK", nargs='?',
                            help="audio chunk to split and convert"
                           )

    argparser.add_argument("cuefile", metavar="CUEFILE",nargs='?',
                            help="audio chunk to split and convert"
                           )

    args  = argparser.parse_args()

    chunk   = args.chunk.decode("utf8") if args.chunk else u""
    cuefile = args.cuefile.decode("utf8") if args.cuefile else u""

    chunk, cuefile = analyze_args ( chunk, cuefile)

    if chunk and cuefile :
        splitwrapper_both(chunk, cuefile)
    elif chunk:
        splitwrapper_only_chunk(chunk)
    elif cuefile:
        splitwrapper_only_cuefile(chunk)
    else:
        splitwrapper_none()

