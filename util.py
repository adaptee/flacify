#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import chardet

from subprocess import call
from color import green, yellow, red
from cuesheet.cueyacc import parsecuedata

from mutagen.flac import FLAC
from mutagen.apev2 import APEv2

support_text_encodings = [  'ascii',
                            'latin1',
                            'utf-8',
                            'cp936', 'gb18030', 'gb2312', 'gbk',
                            'shift_jis',
                         ]

def flac_extractor(audiofile):
    tag = FLAC(audiofile)
    info = { }
    for key in tag.keys():
        # tricky part
        info[key.lower()] = tag[key][0]
    return info

def apev2_extractor(audiofile):
    tag = APEv2(audiofile)
    info = { }
    for key in tag.keys():
        # tricky part
        info[key.lower()] = unicode(tag[key])
    return info

extensions = { }
extensions[".flac"] = {
                        "encoder"  : "flac",
                        "decoder"  : "flac",
                        "tagextracter" : flac_extractor,
                        "reminder" : "please install package flac",
                     }

extensions[".ape"] = {
                        "encoder"  : "mac",
                        "decoder"  : "mac",
                        "tagextracter" : apev2_extractor,
                        "reminder" : "please install package mac",
                     }


extensions[".tta"] = {
                        "encoder"  : "ttaenc",
                        "decoder"  : "ttaenc",
                        "tagextracter" : apev2_extractor,
                        "reminder" : "please install package ttaenc",
                     }

extensions[".wv"] = {
                        "encoder"  : "wvpack",
                        "decoder"  : "wvunpack",
                        "tagextracter" : apev2_extractor,
                        "reminder" : "please install package wavpack",
                     }

extensions[".wav"] = {
                        "encoder"  : "ls", # tricky, wav does not need decoder nor encoder
                        "decoder"  : "ls",
                        "tagextracter" : None,
                        "reminder" : "command ls not founded. Are you really using *nix ?",
                     }



class MyException(Exception):

    def __init__(self, *args):
        self.message = args[0]
        super(MyException, self).__init__(args)


class CommandNotFoundError(MyException):
    pass

class EncodingError(MyException):
    pass


def check_command_available( command, reminder="" ):

    commands = "which %s 2>/dev/null >/dev/null" % (command)
    exitcode = call( commands, shell=True)

    if exitcode != 0 :

        msg = "command '%s' is not found." % (command)
        msg += reminder

        raise CommandNotFoundError( msg)

def guess_text_encoding(text):

    guess      = chardet.detect(text)
    encoding   = guess['encoding']
    confidence = guess['confidence']

    if not encoding :
        raise EncodingError("failed to detect the encoding")

    encoding   = encoding.lower()

    if confidence < 0.98 :
        raise EncodingError("encoding detected as '%s', but with low confidence %s"
                            % (encoding, confidence) )
    elif encoding not in support_text_encodings :
        raise EncodingError("encoding '%s' is not well supported yet."
                            % encoding )
    else:
        if encoding in ['gbk', 'gb2312', 'cp936' ] :
            encoding = 'gb18030'

        return encoding

def conv2unicode(text):

    if type(text) == unicode :
        return text

    encoding = guess_text_encoding(text)
    result   = unicode( text.decode(encoding) )

    return result


def parsecuefile(cuefile):

    cuedata = open(cuefile).read()
    infomsg ( ("parsing cuefile: %s...") % (cuefile) )

    cuedata = conv2unicode(cuedata)
    return parsecuedata(cuedata)

def normalize_filename(filename):
    """
        fix invalid chars within filename
    """

    # "/"  is invalid in filename
    filename = filename.replace( "/", "-")

    return filename


def infomsg (text):
    print (green( "[info] %s" % (text) ) )

def warnmsg (text):
    print (yellow( "[warning] %s" % (text) ) )

def errormsg (text):
    print (red( "[error] %s" % (text) ) )


