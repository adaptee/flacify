#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from subprocess import Popen, PIPE
from glob import glob
from mutagen.flac import FLAC

from cueyacc import parsecuefile
from cuesheet import CueSheet

glob_pattern = "split-*.flac"


def split(chunk, cuesheet):

    splitchunk(chunk, cuesheet)

    pieces = glob(glob_pattern)

    tagpieces(pieces, cuesheet)


    rename(pieces)

    pass


def splitchunk ( chunk, cuesheet):

    command =  "shnsplit -O never -o flac %s " % (chunk,)
    pipe = Popen( command, shell=True, stdin=PIPE, stdout=PIPE )

    pipe.stdin.write(cuesheet.showbreakpoints())
    pipe.stdin.close()
    output = pipe.stdout.read()

    print (output)

def tagpieces(pieces, cuesheet):
    number = 1

    for piece in pieces:
        tagpiece(piece, number, cuesheet)
        number += 1

def tagpiece(piece, number, cuesheet):

    audio = FLAC(piece)

    audio["title"]       = cuesheet.tracks[number-1].title
    audio["artist"]      = cuesheet.tracks[number-1].performer

    audio["album"]       = cuesheet.title
    audio["date"]        = cuesheet.date
    #audio["genre"]       = cuesheet.genre

    #audio["tracknumber"] = number
    #audio["totaltracks"] = len(cuesheet.tracks)

    #audio["comment"]      = ""
    #audio["performer"]    = ""
    #audio["composer"]     = ""
    #audio["album artist"] = ""
    #audio["encoded-by"]   = ""
    #audio["discnumber"]   = ""

    audio.save()

def renamepieces(pieces):

    for piece in pieces:
        renamepiece(piece)

def renamepiece(piece):

    audio = FLAC(piece)

    tracknumber = audio["tracknumber"][0]
    title       = audio["title"][0]

    goodname = "%02d. %s" % (tracknumber, title)
    os.rename(piece, goodname)


if __name__ == "__main__" :

    CHUNK='1.ape'
    CUE="1.cue"
    cuesheet = parsecuefile(CUE)

    #splitchunk(CHUNK, cuesheet)

    pieces = glob(glob_pattern)

    tagpieces(pieces, cuesheet)

