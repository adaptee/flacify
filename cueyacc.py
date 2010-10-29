#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import ply.yacc as yacc

# Get the token map from the correspoding lexer.  This is required.
from cuelex import tokens
from cuesheet import CueSheet, createCueSheet, createTrackInfo

#def p_empty(p):
    #'empty :'
    #pass

# Error rule for syntax errors
def p_error(p):
    print (p)
    print ("Syntax error in input!")

def p_cuesheet(p):
    r' cuesheet : topentries file'

    infopairs = p[1] + p[2]
    table     = { }

    for infopair in infopairs:
        key        = infopair[0]
        value      = infopair[1]
        table[key] = value

    #print table
    p[0] = createCueSheet(table)

def p_topentries(p):
    r'''
    topentries : topentries topentry
               | topentry
    '''
    if len(p) == 3 :
        p[0] = p[1] + [p[2],]
    else:
        p[0] = [ p[1] ]

def p_topentry(p):
    r'''
    topentry : catalog
             | cdtextfile
             | title
             | flags
             | performer
             | genre
             | comment
             | date
             | discid
    '''
    p[0] =  p[1]

def p_file(p):
    r'file : FILE VALUE FILETYPE tracks '

    filename = p[2]
    tracks = p[4]

    p[0] = [ ("file", filename), ("tracks", tracks) ]

def p_tracks(p):
    r'''tracks : tracks track
               | track
    '''

    if len(p) == 3 :
        # '+' apply to two list, so it's tricky here
        p[0] = p[1] + [ p[2], ]
    else:
        p[0] = [ p[1], ]

def p_track(p):
    r'track : TRACK NUMBER TRACKTYPE subentries '

    number    = p[2]
    infopairs = p[4]

    table = { }
    table["number"] = number

    for infopair in infopairs:
        key        = infopair[0]
        value      = infopair[1]
        table[key] = value

    p[0] = createTrackInfo(table)

def p_subentries(p):
    r'''
    subentries :  subentries subentry
               |  subentry
    '''

    if len(p) == 3:
        p[0] =  p[1] + [ p[2], ]
    else:
        p[0] = [ p[1], ]

def p_subentry(p):
    r'''
    subentry : title
             | performer
             | isrc
             | index
             | flags
             | songwriter
             | postgap
             | pregap
    '''
    p[0] =  p[1]

def p_catalog(p):
    r'catalog : CATALOG VALUE'
    p[0] = ( 'catalog', p[2])

def p_cdtextfile(p):
    r'cdtextfile : CDTEXTFILE VALUE'
    p[0] = ( 'cdtextfile', p[2])

def p_postgap(p):
    r'postgap : POSTGAP TIME'
    p[0] = ( 'postgap', p[2])

def p_pregap(p):
    r'pregap : PREGAP TIME'
    p[0] = ( 'pregap', p[2])

def p_songwriter(p):
    r'songwriter : SONGWRITER VALUE'
    p[0] = ( 'songwriter', p[2])

def p_title(p):
    r'title : TITLE VALUE'
    p[0] = ('title', p[2] )

def p_performer(p):
    r'performer : PERFORMER VALUE'
    p[0] = ('performer', p[2] )

def p_isrc(p):
    r'isrc : ISRC ISRCID'
    p[0] = ('isrc', p[2])

def p_index(p):
    r'index : INDEX NUMBER TIME'

    number = p[2]
    # offfset00, offset01, etc
    key = "offset%02d" % (int(number),)
    offset = p[3]

    p[0] = (key, offset )

def p_flags(p):
    r'flags : FLAGS VALUE'
    p[0] = ('flags', p[2] )

def p_genre(p):
    r' genre :  REM GENRE VALUE '
    p[0] = ( 'genre', p[3] )

def p_comment(p):
    r' comment :  REM COMMENT VALUE '
    p[0] = ( 'comment', p[3] )

def p_date(p):
    r' date :  REM DATE DATEVALUE '
    p[0] = ( 'date', p[3] )

def p_discid(p):
    r' discid :  REM DISCID VALUE '
    p[0] = ( 'discid', p[3] )


# Build the parser
cueparser = yacc.yacc()


def parsecuefile(cuefile):
    data = open(cuefile).read().decode("utf8")
    return cueparser.parse(data)

if __name__ == "__main__" :

    data = u'''
    TITLE "Fate／Recapture -original songs collection-"
    REM COMMENT "hello"
    PERFORMER  "Various Artists"
    FILE "CDImage.ape" WAVE
    TRACK 01 AUDIO
    TITLE "THIS ILLUSION"
    PERFORMER "M.H."
    ISRC 000000000000
    INDEX 01 00:00:00
    '''

    data = open("1.cue").read().decode("utf8")

    result = cueparser.parse(data)
    print result
    print result.showbreakpoints()

    #print result.tracks[1].number
    #print result.tracks[0]

