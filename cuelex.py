#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import ply.lex as lex
from ply.lex import TOKEN

# List of token names.   This is always required
tokens = (
    'CATALOG', 'CDTEXTFILE', 'FILE', 'FLAGS', 'INDEX', 'ISRC', 'PERFORMER',
    'POSTGAP', 'PREGAP', 'REM', 'SONGWRITER', 'TITLE', 'TRACK',

    'FILETYPE', 'TRACKTYPE',
    'OFFSET', 'ISRCID',

    'GENRE', 'COMMENT', 'DATE', 'DISCID',
    'DATEVALUE',

    'NUMBER','VALUE',
)

# Regular expression rules for simple tokens
twodigits = r'\d{2}'
year      = r'(19|20)\d{2}'
date      = year + r'(-|/)' + twodigits + r'(-|/)' + twodigits

# A string containing ignored characters (spaces and tabs and linebreaks)
t_ignore  = ' \t\n'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# the priority order is as-is

#----cuesheet commands
def t_CATALOG(t):
    r'\bCATALOG\b'
    return t

def t_CDTEXTFILE(t):
    r'\bCDTEXTFILE\b'
    return t

def t_FILE(t):
    r'\bFILE\b'
    return t

def t_FLAGS(t):
    r'\bFLAGS\b'
    return t

def t_INDEX(t):
    r'\bINDEX\b'
    return t

def t_ISRC(t):
    r'\bISRC\b'
    return t

def t_PERFORMER(t):
    r'\bPERFORMER\b'
    return t

def t_POSTGAP(t):
    r'\bPOSTGAP\b'
    return t

def t_PREGAP(t):
    r'\bPREGAP\b'
    return t

def t_REM(t):
    r'\bREM\b'
    return t

def t_SONGWRITER(t):
    r'\bSONGWRITER\b'
    return t

def t_TITLE(t):
    r'\bTITLE\b'
    return t

def t_TRACK(t):
    r'\bTRACK\b'
    return t

#----valid FILE type
def t_FILETYPE(t):
    r'\b(AIFF|BINARY|MOTOROLA|MP3|WAVE)\b'
    return t

#----valid track type
def t_TRACKTYPE(t):
    r'\b(AUDIO)\b'
    return t


#--- supported metadata

def t_GENRE(t):
    r'\bGENRE\b'
    return t

def t_COMMENT(t):
    r'\bCOMMENT\b'
    return t

def t_DATE(t):
    r'\bDATE\b'
    return t

def t_DISCID(t):
    r'\bDISCID\b'
    return t

# ---- other expected value
def t_OFFSET(t):
    r'\b\d{2}:\d{2}:\d{2}\b'
    return t

def t_ISRCID(t):
    r'\b[a-zA-Z-0-9]{5}\d{7}\b'
    return t

def t_YEARVALUE(t):
    r'\b(19|20)\d{2}\b'
    return t

@TOKEN(date)
def t_DATEVALUE(t):
    return t

def t_NUMBER(t):
    r'\b\d{2}\b'
    return t

# FIXME
# this implementation only matches quoted value !
def t_VALUE(t):
    r'"[^"\n]+"'
    t.value = t.value.strip('"')
    return t

# Build the lexer
lexer = lex.lex()

if __name__ == '__main__':


    # Test it out

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

    #f  = open("1.cue")
    #data = f.read()


    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok


