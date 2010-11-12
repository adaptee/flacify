#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import mutagen

from mutagen.apev2 import APEv2
from mutagen.flac import FLAC

class LossLess(object):

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

        tagproxy = self.TagProxy(self.filename)

        for key in kwargs.keys():
            tagproxy[key] = kwargs[key]

        tagproxy.save()

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

class FLACFormat(LossLess):

    TagProxy = FLAC

    extension = ".flac"
    encoder   = "flac"
    decoder   = "flac"
    reminder  = "please install package 'flac'. "


    def __init__(self, filename):
        super(FLACFormat, self).__init__(filename)

    def extract_taginfo(self):
        taginfo  = { }

        tagproxy = FLAC(self.filename)
        for key in tagproxy.keys():
            taginfo[key.lower()] = tagproxy[key][0]

        return taginfo


class APEFormat(LossLess):

    TagProxy = APEv2

    extension = ".ape"
    encoder   = "mac"
    decoder   = "mac"
    reminder  = "please install package 'mac'. "

    def __init__(self, filename):
        super(APEFormat, self).__init__(filename)

    def extract_taginfo(self):
        taginfo  = { }

        tagproxy = APEv2( self.filename)
        for key in tagproxy.keys():
            taginfo[key.lower()] = unicode(tagproxy[key])

        return taginfo

class TTAFormat(LossLess):

    TagProxy = APEv2

    extension = ".tta"
    encoder   = "ttaenc"
    decoder   = "ttaenc"
    reminder  = "please install package 'ttaenc'. "

    def __init__(self, filename):
        super(TTAFormat, self).__init__(filename)

    def extract_taginfo(self):
        taginfo  = { }

        tagproxy = APEv2( self.filename)
        for key in tagproxy.keys():
            taginfo[key.lower()] = unicode(tagproxy[key])

        return taginfo

class WVFormat(LossLess):

    TagProxy = APEv2

    extension = ".wv"
    encoder   = "wvpack"
    decoder   = "wvunpack"
    reminder  = "please install package 'wavpack'. "

    def __init__(self, filename):
        super(WVFormat, self).__init__(filename)

    def extract_taginfo(self):
        taginfo  = { }

        tagproxy = APEv2( self.filename)
        for key in tagproxy.keys():
            taginfo[key.lower()] = unicode(tagproxy[key])

        return taginfo

class WAVFormat(LossLess):

    extension = ".wv"
    encoder   = "ls"
    decoder   = "ls"
    reminder  = ""

    def __init__(self, filename):
        super(WAVFormat, self).__init__(filename)

    def extract_taginfo(self):
        # .wav format does support taginfo
        return None

    def update_taginfo(self, **kwargs):
        pass

lossless_formats = {
                        ".flac": FLACFormat,
                        ".ape" : APEFormat,
                        ".tta" : TTAFormat,
                        ".wv"  : WVFormat,
                        ".wav" : WAVFormat,
                   }

def getLossLessFormat(filename):
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    format = lossless_formats.get(ext)

    if not format :
        raise ValueError("format %s is not supported." % ext)

    return format(filename)

