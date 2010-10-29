#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os

from subprocess import Popen, PIPE
from glob import glob
from mutagen.flac import FLAC

from cueyacc import parsecuefile
from cuesheet import CueSheet

pieces_pattern = "split-*.flac"

def pickcuefile(chunk):

    basename, extenseion = os.path.splitext(chunk)

    candicates = glob( ( "%s*.cue" % basename) )

    # FIXME
    bestchoice =  basename + ".cue"

    return bestchoice


def convert(audio):
    pass

def split(chunk, cuesheet):

    splitchunk(chunk, cuesheet.breakpoints() )

    pieces = glob(pieces_pattern)
    tagpieces(pieces, cuesheet)

    #renamepieces(pieces)


def splitchunk ( chunk, breakpoints):

    # FIXME
    # when shnspilt's stdin is connected to PIPE
    # it can't prompt user to make choice
    command =  "shnsplit -O never -o flac %s " % (chunk,)
    pipe = Popen( command, shell=True, stdin=PIPE, stdout=PIPE )

    pipe.stdin.write(breakpoints)
    pipe.stdin.close()
    output = pipe.stdout.read()

    print (output)

def tagpieces(pieces, cuesheet):

    number = 1

    for piece in pieces:
        track = cuesheet.track(number)
        tagpiece(piece, track)

        number += 1

def tagpiece(piece, track):

    audio = FLAC(piece)

    audio["title"]       = track.title()
    audio["artist"]      = track.artist()
    audio["album"]       = track.album()
    audio["date"]        = track.date()
    audio["genre"]       = track.genre()

    audio["tracknumber"] = track.tracknumber()
    audio["tracktotal"] = str(track.tracktotal())

    audio["comment"]      = track.comment()

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

    # tricky
    # the retrived value is a list containg one unicode string
    title       = audio["title"][0]
    tracknumber = int (audio["tracknumber"][0] )

    goodname = "%02d. %s.flac" % (tracknumber, title)
    os.rename(piece, goodname)


if __name__ == "__main__" :


    chunk    = '1.ape'
    cuesheet = parsecuefile("1.cue")

    split(chunk, cuesheet)


