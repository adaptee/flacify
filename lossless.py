#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import subprocess
import glob

from mutagen.apev2 import APEv2
from mutagen.flac  import FLAC

from cuesheet.cueyacc import parsecuedata
from util  import check_command_available, MyException, \
           infomsg, warnmsg, parsecuefile, conv2unicode
from util  import normalize_filename, NoCuedataError

class ShntoolError(MyException):
    pass

class ReplayGainError(MyException):
    pass

def shnconv(filename, format="flac"):
    command  = [ 'shntool', 'conv', '-o', format, filename ]
    exitcode = subprocess.call( command, shell=False)

    if exitcode != 0:
        raise ShntoolError("shntool failed to convert %s into %s format"
                            % (filename, format) )

def shnsplit ( filename, breakpoints, format="flac" ):

    pipe = subprocess.Popen( ['shnsplit', '-O', 'never', '-o', format, filename ],
                  shell=False, stdin=subprocess.PIPE)

    pipe.stdin.write(breakpoints)
    pipe.stdin.close()

    exitcode = pipe.wait()

    if exitcode != 0 :
        raise ShntoolError("shntool failed to split %s into %s pieces"
                            %(filename, format) )

    pieces_pattern = "split-track*.%s" % format

    pieces = glob.glob(pieces_pattern)
    return sorted(pieces)

def eval_scheme(scheme, taginfo):

    scheme = scheme.replace("%a" , taginfo.get("artist"      , "") )
    scheme = scheme.replace("%A" , taginfo.get("album"       , "") )
    scheme = scheme.replace("%g" , taginfo.get("genre"       , "") )
    scheme = scheme.replace("%t" , taginfo.get("title"       , "") )
    scheme = scheme.replace("%y" , taginfo.get("date"        , "") )

    scheme = scheme.replace("%n" , "%02d" % int(taginfo.get("tracknumber" , "") ))

    return scheme

default_scheme = "%n. %t"

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
    def calcReplayGain(cls, pieces):
        pass

    @staticmethod
    def tag_pieces(pieces, cuesheet):

        number = 1

        for piece in pieces:

            track  = cuesheet.track(number)
            target = getLossLessAudio(piece)
            target.update_taginfo_from_cueinfo(track)

            number += 1

    @staticmethod
    def rename_pieces(pieces, scheme=default_scheme):
        infomsg( "renaming pieces...")

        for piece in pieces:
            target = getLossLessAudio(piece)
            target.rename_by_taginfo(scheme)

    def __init__(self, filename):
        self.filename  = filename
        self.basename  = os.path.splitext(filename)[0]

    # dummy method
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
        return taginfo.get("cuesheet", "")

    def embeded_image(self):
        pass

    def split (self, cuefile,  cmd_args ):

        format = cmd_args.format if cmd_args.format else "flac"
        scheme = cmd_args.scheme if cmd_args.scheme else default_scheme

        target = getLossLessAudio("xyz." + format)

        self.check_decodable()
        target.check_encodable()

        try :
            cuesheet = parsecuefile( cuefile)
        except NoCuedataError as e:
            # when no cuefile is not available
            infomsg( e.message)
            infomsg("trying embeded cuesheet...")
            cuedata = self.embeded_cuedata()
            if not cuedata :
                raise NoCuedataError("%s does not contain embeded cuedata."
                                     % self.filename )
            cuesheet = parsecuedata( conv2unicode(cuedata) )

        infomsg( "splitting audio chunk: %s..." % self.filename)
        pieces = shnsplit(self.filename, cuesheet.breakpoints(), format)

        target.tag_pieces(pieces, cuesheet)
        target.calcReplayGain(pieces)

        target.rename_pieces(pieces, scheme)

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

    def update_taginfo_from_cueinfo(self, track):
        taginfo = { }

        #taginfo["title"]       = track.title()
        #taginfo["artist"]      = track.artist()
        #taginfo["album"]       = track.album()
        #taginfo["date"]        = track.date()
        #taginfo["genre"]       = track.genre()
        #taginfo["tracknumber"] = track.tracknumber()
        #taginfo["tracktotal"]  = str(track.tracktotal())
        #taginfo["comment"]     = track.comment()

        taginfo["title"]       = track.title
        taginfo["artist"]      = track.artist
        taginfo["album"]       = track.album
        taginfo["date"]        = track.date
        taginfo["genre"]       = track.genre
        taginfo["tracknumber"] = track.tracknumber
        taginfo["tracktotal"]  = str(track.tracktotal)
        taginfo["comment"]     = track.comment
        self.update_taginfo(**taginfo)


    def rename_by_taginfo(self, scheme=default_scheme):

        taginfo = self.extract_taginfo()

        filename = "%s%s" % ( eval_scheme(scheme, taginfo),
                               self.extension,
                             )

        filename_good = normalize_filename(filename)
        infomsg ("filename_good: %s => %s" % (self.filename, filename_good))

        os.rename(self.filename, filename_good)

        self.filename = filename_good
        self.basename = os.path.splitext(filename_good)[0]

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

    @classmethod
    def calcReplayGain(cls, pieces):

        command = ['metaflac', '--add-replay-gain' ]
        command.extend(pieces)

        return

        infomsg( "calculating replaygain info for flac files...")

        exitcode = subprocess.call( command,
                                    shell=False,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE
                                   )

        if exitcode != 0:
            raise ReplayGainError( "fail to calulate replaygain for flac files. ")


    def __init__(self, filename):
        super(FLACAudio, self).__init__(filename)

    def extract_taginfo(self):
        taginfo  = { }

        try :
            tagproxy = FLAC(self.filename)
        except ValueError :
            return { }

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
        except ValueError :
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

    @classmethod
    def calcReplayGain(cls, pieces):

        command = ['wvgain', '-a' ]
        command.extend(pieces)

        infomsg( "calculating replaygain info for wavpack files...")

        exitcode = subprocess.call( command,
                                    shell=False,
                                    stdout=subprocess.PIPE,
                                   )

        if exitcode != 0:
            raise ReplayGainError( "fail to calulate replaygain for wavpack files. ")

    def __init__(self, filename):
        super(WVAudio, self).__init__(filename)

    def extract_taginfo(self):

        try :
            tagproxy = APEv2( self.filename)
        except ValueError:
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
        return { }

    def update_taginfo(self, **kwargs):
        return

    def rename_by_taginfo(self, scheme=default_scheme):
        # .wav format dose not support taginfo
        return

    def convert2wav(self):
        warnmsg("%s is already in %s format." % (self.filename, self.format) )


lossless_formats = {
                        ".flac": FLACAudio,
                        ".ape" : APEAudio,
                        ".tta" : TTAAudio,
                        ".wv"  : WVAudio,
                        ".wav" : WAVAudio,
                   }

lossless_extensions = [ '.ape', '.flac', '.tta', '.wv', '.wav', ]

class FormatError(MyException):
    pass

def getLossLessAudio(filename):
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    try:
        format = lossless_formats[ext]
        return format(filename)
    except KeyError :
        raise FormatError("format %s is not supported." % ext)
