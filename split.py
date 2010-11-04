#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os

from glob import glob
from subprocess import Popen, PIPE, call

from mutagen.flac import FLAC
from cuesheet.cueyacc import parsecuedata
from cuesheet.cuesheet import CueSheet
from util import infomsg, check_audio_decodable, parsecuefile

pieces_pattern = "split-*.flac"

def split(chunk, cuesheet):

    check_audio_decodable(chunk)

    chunk2pieces(chunk, cuesheet.breakpoints() )

    pieces = glob(pieces_pattern)

    tagpieces(pieces, cuesheet)

    calc_replaygain(pieces)

    renamepieces(pieces)

def chunk2pieces ( chunk, breakpoints):

    # FIXME
    # when shnspilt's stdin is connected to PIPE
    # it can't prompt user to make choice interactively

    # Use shell=False to preventing shell to get in the way
    # Instead, command is executed directly through execve()
    # This avoids the annoying problem of quoting filename
    pipe = Popen( ['shnsplit', '-O', 'never', '-o', 'flac', chunk ] ,
                  shell=False, stdin=PIPE, stdout=PIPE)

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

def calc_replaygain( pieces):

    command = ['metaflac', '--add-replay-gain' ]
    command.extend(pieces)

    infomsg( "calculating replaygain info...")

    code = call( command, shell=False, stdin=PIPE, stdout=PIPE)



if __name__ == "__main__" :

    cuesheet = parsecuefile("1.cue")

    split("1.wav", cuesheet)


