#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os

from mutagen.apev2 import APEv2
from mutagen.flac import FLAC

class LossLessAudio(object):

    # A proxy class for accessing taginfo
    TagProxy  = None

    extension = ""
    encoder   = ""
    decoder   = ""
    reminder  = ""

    def __init__(self, filename):
        self.filename  = filename

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

    def embeded_cuesheet(self):
        taginfo = self.extract_taginfo()
        return taginfo.get("cuesheet")

    def embeded_image(self):
        pass

    def chunk2pieces (self, cuesheet=None):
        pass

    def convert2flac(self):
        pass

    def debug_repr(self):
        pass

class FLACAudio(LossLessAudio):

    TagProxy = FLAC

    extension = ".flac"
    encoder   = "flac"
    decoder   = "flac"
    reminder  = "please install package 'flac'. "


    def __init__(self, filename):
        super(FLACAudio, self).__init__(filename)

    def extract_taginfo(self):
        taginfo  = { }

        tagproxy = FLAC(self.filename)
        for key in tagproxy.keys():
            taginfo[key.lower()] = tagproxy[key][0]

        return taginfo


class APEAudio(LossLessAudio):

    TagProxy = APEv2

    extension = ".ape"
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

class TTAAudio(LossLessAudio):

    TagProxy = APEv2

    extension = ".tta"
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

class WVAudio(LossLessAudio):

    TagProxy = APEv2

    extension = ".wv"
    encoder   = "wvpack"
    decoder   = "wvunpack"
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

class WAVAudio(LossLessAudio):

    extension = ".wv"
    encoder   = "ls"
    decoder   = "ls"
    reminder  = ""

    def __init__(self, filename):
        super(WAVAudio, self).__init__(filename)

    def extract_taginfo(self):
        # .wav format does support taginfo
        return None

    def update_taginfo(self, **kwargs):
        pass


lossless_formats = {
                        ".flac": FLACAudio,
                        ".ape" : APEAudio,
                        ".tta" : TTAAudio,
                        ".wv"  : WVAudio,
                        ".wav" : WAVAudio,
                   }

def getLossLessAudio(filename):
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    format = lossless_formats.get(ext)

    if not format :
        raise ValueError("format %s is not supported." % ext)

    return format(filename)

