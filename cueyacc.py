#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""

"""

import ply.yacc as yacc

# Get the token map from the correspoding lexer.  This is required.
from cuelex import tokens

start = 'file'

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

#def p_empty(p):
    #'empty :'
    #pass

def topentry(p):
    r'''
    topentry : catalog
               cdtextfile
               flags
               isrc
               performer
               postgap
               pregap
               rem
               songwriter
               title
    '''
    p[0] = p[1]



def p_file(p):
    r'file : FILE VALUE FILETYPE tracks '
    p[0] = ( p[2], p[3], p[4])


def p_tracks(p):
    r'''tracks : tracks track
               | track
    '''

    if len(p) == 3 :
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_track(p):
    r'track : TRACK NUMBER TRACKTYPE subentries '
    p[0] = ( p[2], p[4] )


def p_subentries(p):
    r'''
    subentries :  subentries subentry
               |  subentry
    '''

    if len(p) == 3:
        p[0] =  p[1] + p[2]
    else:
        p[0] = p[1]

def p_subentry(p):
    r'''
    subentry : title
             | performer
             | isrc
             | index
             | flags
    '''

    p[0] = [ p[1] ]

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
    r'index : INDEX NUMBER OFFSET'
    p[0] = ('offset', p[3] )

def p_flags(p):
    r'flags : FLAGS VALUE'
    p[0] = ('flags', p[2] )

#def p_catalog(p):
    #r'catalog : CATALOG VALUE'


#def p_cdtextfile(p):
    #r'catalog : CDTEXTFILE VALUE'


#def p_genre(p):
    #r'genre : REM GENRE VALUE'


if __name__ == "__main__" :

    # Build the parser
    parser = yacc.yacc()

    #data = u'''
    #TITLE "days"
    #PERFORMER "CHINO"
    #ISRC 000000000000
    #INDEX 01 04:11:68
    #FLAGS PRE
    #'''

    data = u'''
    FILE "CDImage.ape" WAVE
    TRACK 01 AUDIO
    TITLE "THIS ILLUSION"
    PERFORMER "M.H."
    ISRC 000000000000
    INDEX 01 00:00:00

    TRACK 02 AUDIO
    TITLE "days"
    PERFORMER "CHINO"
    ISRC 000000000000
    INDEX 01 04:11:68

    TRACK 03 AUDIO
    TITLE "memory"
    PERFORMER "M.H."
    ISRC 000000000000
    INDEX 01 08:37:18
    '''

    result = parser.parse(data)
    print result

