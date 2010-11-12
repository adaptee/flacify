#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import chardet

from subprocess import call
from color import green, yellow, red
from cuesheet.cueyacc import parsecuedata

from mutagen.flac import FLAC
from mutagen.apev2 import APEv2

supported_encodings = [ 'ascii',
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

class FormatNotSupportedError(MyException):
    pass

class EncodingNotDetectedError(MyException):
    pass

class EncodingNotSupportedError(MyException):
    pass


def check_command_available( command, reminder="" ):

    commands = "which %s 2>/dev/null >/dev/null" % (command)
    exitcode = call( commands, shell=True)

    if exitcode != 0 :

        msg = "command '%s' is not found." % (command)
        msg += reminder

        raise CommandNotFoundError( msg)

def check_audio_decodable(filename):

    _, ext = os.path.splitext(filename)
    ext    = ext.lower()

    try :
        extension = extensions[ext]
        check_command_available ( extension["decoder"] )
    except KeyError as e:
        errormsg( "format '%s' is not supported" % (e) )
        os.sys.exit(1)
    except CommandNotFoundError as e :
        errormsg( e.message)
        os.sys.exit(1)

def guess_text_encoding(text):

    guess      = chardet.detect(text)
    encoding   = guess['encoding']
    confidence = guess['confidence']

    if not encoding :
        raise EncodingNotDetectedError("failed to detect the encoding")

    encoding = encoding.lower()

    if encoding in supported_encodings and confidence >= 0.98 :
        if encoding in ['gbk', 'gb2312', 'cp936',] :
            return 'gb18030'
        else:
            return encoding
    else:
        raise EncodingNotSupportedError(encoding)

def conv2unicode(text):

    if type(text) == unicode :
        return text

    encoding = guess_text_encoding(text)
    result   = unicode( text.decode(encoding) )
    return result


def parsecuefile(cuefile):
    infomsg ( ("parsing cuesheet: %s...") % (cuefile) )

    cuedata = open(cuefile).read()
    try :
        cuedata = conv2unicode(cuedata)
        return parsecuedata(cuedata)
    except EncodingNotSupportedError as e:
        infomsg(
                "The encoding of '%s' is '%s', which is not well supported.\
                Please change its encoding to UTF-8 manually."
                % (cuefile, e.message)
               )
        os.sys.exit(1)

def infomsg (text):
    print (green( "[info] %s" % (text) ) )

def warnmsg (text):
    print (yellow( "[warning] %s" % (text) ) )

def errormsg (text):
    print (red( "[error] %s" % (text) ) )



