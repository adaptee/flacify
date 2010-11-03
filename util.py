#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
from subprocess import call
from color import green

extensions = { }
extensions[".ape"] = {
                        "encoder"  : "mac",
                        "decoder"  : "mac",
                        "errormsg" : "please install package mac",
                     }

extensions[".flac"] = {
                        "encoder"  : "flac",
                        "decoder"  : "flac",
                        "errormsg" : "please install package flac",
                     }

extensions[".tta"] = {
                        "encoder"  : "ttaenc",
                        "decoder"  : "ttaenc",
                        "errormsg" : "please install package ttaenc",
                     }

extensions[".wv"] = {
                        "encoder"  : "wavpack",
                        "decoder"  : "wavunpack",
                        "errormsg" : "please install package wavpack",
                     }

extensions[".wav"] = {
                        "encoder"  : "ls", # tricky, wav does not need decoder nor encoder
                        "decoder"  : "ls",
                        "errormsg" : "command ls not founded. Are you really using *nix ?",
                     }

class CommandNotFoundError(Exception):
    pass

class FormatNotSupportedError(Exception):
    pass

def check_command_available( command):

    commands = "which %s 2>/dev/null >/dev/null" % (command)
    exitcode = call( commands, shell=True)

    if exitcode != 0 :

        msg = "command '%s' is not found." % (command)
        raise CommandNotFoundError( msg)


def check_audio_decodable(filename):

    _, ext = os.path.splitext(filename)
    ext    = ext.lower()

    try :
        extension = extensions[ext]
        check_command_available ( extension["decoder"] )
    except KeyError as e:
        infomsg( "format '%s' is not supported" % (e.message) )
        os.sys.exit(1)
    except CommandNotFoundError as e :
        infomsg( e.message)
        os.sys.exit(1)


def infomsg (text):
    print green(text)

def strip(text):
    """
        strip leading & trailing whitespaces, single/double quotes
    """

    return text.strip().strip("'").strip('"')

