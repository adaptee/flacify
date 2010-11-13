#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import subprocess
import chardet

from color import green, yellow, red
from cuesheet.cueyacc import parsecuedata

class MyException(Exception):

    def __init__(self, *args):
        self.message = args[0]
        super(MyException, self).__init__(args)

class CommandNotFoundError(MyException):
    pass

class EncodingError(MyException):
    pass

support_text_encodings = [  'ascii',
                            'latin1',
                            'utf-8',
                            'cp936', 'gb18030', 'gb2312', 'gbk',
                            'shift_jis',
                         ]

def check_command_available( command, reminder="" ):

    commands = "which %s 2>/dev/null >/dev/null" % (command)
    exitcode = subprocess.call( commands, shell=True)

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


