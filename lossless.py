#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import subprocess
import glob

from mutagen.apev2 import APEv2
from mutagen.flac import FLAC

from cuesheet.cueyacc import parsecuedata
from util import check_command_available, MyException, infomsg, warnmsg, parsecuefile, conv2unicode
from split import tagpieces, calc_replaygain, renamepieces

class ShntoolError(MyException):
    pass

def shnconv(filename, format="flac"):
    command  = [ 'shntool', 'conv', '-o', format, filename ]
    exitcode = subprocess.call( command, shell=False)

    if exitcode != 0:
        raise ShntoolError("shntool failed to convert %s into %s format" % (filename, format) )

def shnsplit ( filename, breakpoints, format="flac" ):

    pipe = subprocess.Popen( ['shnsplit', '-O', 'never', '-o', format, filename ],
                  shell=False, stdin=subprocess.PIPE)

    pipe.stdin.write(breakpoints)
    pipe.stdin.close()

    exitcode = pipe.wait()

    if exitcode != 0 :
        raise ShntoolError("shntool failed to split %s into %s pieces"
                            %(filename, foramt) )

    pieces_pattern = "split-track*.flac"

    pieces = glob.glob(pieces_pattern)
    return sorted(pieces)



class LossLessAudio(object):

    # A proxy class for accessing taginfo
    TagProxy  = None

    extension = ""
    format    = ""

    encoder   = ""
    decoder   = ""
    gainer    = ""
    reminder  = ""

    @classmethod
    def check_encodable(cls):
        check_command_available(cls.encoder, cls.reminder)

    @classmethod
    def check_decodable(cls):
        check_command_available(cls.decoder, cls.reminder)

    @classmethod
    def replay_gain(cls, files):
        pass

    def __init__(self, filename):
        self.filename  = filename
        self.basename  = os.path.splitext(filename)[0]

    # derived classes need to implement this method
    def extract_taginfo(self):
        pass

    def update_taginfo(self, **kwargs):

        try :
            tagproxy = self.TagProxy(self.filename)
        except ValueError as e:
            # previous line may fail when the file does not contain tag yet.
            # this line implies overwriting.
            tagproxy = self.TagProxy()

        for key in kwargs.keys():
            tagproxy[key] = kwargs[key]

        tagproxy.save(self.filename)

    def embeded_cuedata(self):
        taginfo = self.extract_taginfo()
        return taginfo.get("cuesheet")

    def embeded_image(self):
        pass

    def split (self, cuefile=None, format="flac" ):

        pseudo_target = getLossLessAudio(self.basename + "." + format)
        self.check_decodable()
        pseudo_target.check_encodable()

        try :
            cuesheet = parsecuefile( cuefile)
        except TypeError as e:
            # if no cuefile is provided.
            infomsg("trying embeded cuesheet...")
            cuedata = self.embeded_cuedata()
            cuesheet = parsecuedata( conv2unicode(cuedata) )

        pieces = shnsplit(self.filename, cuesheet.breakpoints(), format)

        tagpieces(pieces, cuesheet)
        calc_replaygain(pieces)
        renamepieces(pieces)

    def convert(self, format="flac"):

        target = getLossLessAudio(self.basename + "." + format)

        # avoid un-necessary work
        if self.format == target.format :
            warnmsg("%s is already in %s format." % (self.filename, self.format) )
            return

        self.check_decodable()
        target.check_encodable()

        shnconv(self.filename, format)

        self._copy_taginfo(target)

    def _copy_taginfo(self, target):
        taginfo = self.extract_taginfo()
        target.update_taginfo(**taginfo)

    def convert2flac(self):
        self.convert("flac")

    def convert2ape(self):
        self.convert("ape")

    def convert2tta(self):
        self.convert("tta")

    def convert2wv(self):
        self.convert("wv")

    def convert2wav(self):
        self.convert("wav")

    def debug_repr(self):
        pass

class FLACAudio(LossLessAudio):

    TagProxy = FLAC

    extension = ".flac"
    format    = "FLAC"

    encoder   = "flac"
    decoder   = "flac"
    gainer    = "metaflac"
    reminder  = "please install package 'flac'. "


    def __init__(self, filename):
        super(FLACAudio, self).__init__(filename)

    def extract_taginfo(self):
        taginfo  = { }

        tagproxy = FLAC(self.filename)
        for key in tagproxy.keys():
            taginfo[key.lower()] = tagproxy[key][0]

        return taginfo

    def convert2flac(self):
        warnmsg("%s is already in %s format." % (self.filename, self.format) )


class APEAudio(LossLessAudio):

    TagProxy = APEv2

    extension = ".ape"
    format    = "APE"
    encoder   = "mac"
    decoder   = "mac"
    reminder  = "please install package 'mac'. "

    def __init__(self, filename):
        super(APEAudio, self).__init__(filename)

    def extract_taginfo(self):

        try :
            tagproxy = APEv2( self.filename)
        except ValueError as e:
            return  { }

        taginfo  = { }
        for key in tagproxy.keys():
            taginfo[key.lower()] = unicode(tagproxy[key])

        return taginfo

    def convert2ape(self):
        warnmsg("%s is already in %s format." % (self.filename, self.format) )

class TTAAudio(LossLessAudio):

    TagProxy = APEv2

    extension = ".tta"
    format    = "TTA"
    encoder   = "ttaenc"
    decoder   = "ttaenc"
    reminder  = "please install package 'ttaenc'. "

    def __init__(self, filename):
        super(TTAAudio, self).__init__(filename)

    def extract_taginfo(self):

        try :
            tagproxy = APEv2( self.filename)
        except ValueError as e:
            return  { }

        taginfo  = { }
        for key in tagproxy.keys():
            taginfo[key.lower()] = unicode(tagproxy[key])

        return taginfo

    def convert2tta(self):
        warnmsg("%s is already in %s format." % (self.filename, self.format) )

class WVAudio(LossLessAudio):

    TagProxy = APEv2

    extension = ".wv"
    format    = "WavPack"
    encoder   = "wavpack"
    decoder   = "wvunpack"
    gainer    = "wvgain"
    reminder  = "please install package 'wavpack'. "

    def __init__(self, filename):
        super(WVAudio, self).__init__(filename)

    def extract_taginfo(self):

        try :
            tagproxy = APEv2( self.filename)
        except ValueError as e:
            return  { }

        taginfo  = { }
        for key in tagproxy.keys():
            taginfo[key.lower()] = unicode(tagproxy[key])

        return taginfo

    def convert2wv(self):
        warnmsg("%s is already in %s format." % (self.filename, self.format) )

class WAVAudio(LossLessAudio):

    extension = ".wav"
    format    = "Wave"
    encoder   = "ls"
    decoder   = "ls"
    reminder  = "command ls not founded. Are you really using *nix ?"

    def __init__(self, filename):
        super(WAVAudio, self).__init__(filename)

    def extract_taginfo(self):
        # .wav format does support taginfo
        return None

    def update_taginfo(self, **kwargs):
        pass

    def convert2wav(self):
        warnmsg("%s is already in %s format." % (self.filename, self.format) )


lossless_formats = {
                        ".flac": FLACAudio,
                        ".ape" : APEAudio,
                        ".tta" : TTAAudio,
                        ".wv"  : WVAudio,
                        ".wav" : WAVAudio,
                   }

class FormatError(MyException):
    pass

def getLossLessAudio(filename):
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    try:
        format = lossless_formats[ext]
        return format(filename)
    except KeyError as e:
        raise FormatError("format %s is not supported." % ext)
