#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import sys

import ply.lex as lex
from ply.lex import TOKEN

# List of token names.   This is always required
tokens = (
    'CATALOG', 'CDTEXTFILE', 'FILE', 'FLAGS', 'INDEX', 'ISRC', 'PERFORMER',
    'POSTGAP', 'PREGAP', 'REM', 'SONGWRITER', 'TITLE', 'TRACK',

    'CATALOGID', 'FILETYPE', 'TRACKTYPE','FLAGSVALUE',
    'ISRCID', 'TIME',

    'REMKEYWORD',

    'NUMBER','VALUE',
)

#states = (
            #( 'rem', 'exclusive'),
         #)

# Regular expression rules for simple tokens
twodigits = r'\d{1,2}'
year      = r'(19|20)\d{2}'
delimiter = r'[/.-]'
date      = year + r'[/-]' + twodigits + r'[/-]' + twodigits
datevalue = r'(' + r'\b' + year + r'\b' + r'|' + r'\b' + date + r'\b' + r')'

datevalue = r'\b' + year + \
            r'(' + delimiter + twodigits + delimiter + twodigits + r')' + r'?'


quoted_value   = r'"[^"\r\n]*"'
unquoted_value = r'[^"\r\n]+'
value = r'(' + quoted_value + '|' + unquoted_value + ')'

# A string containing ignored characters
# (spaces, tab, CR, NL )
t_ignore  = ' \t\r\n'

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
# In practice, some cuesheet contain lower-case values

def t_CATALOGID(t):
    r'\b\d{13}\b'
    return t

def t_FILETYPE(t):
    r'\b(AIFF|BINARY|MOTOROLA|MP3|WAVE|wave|ape|WAV|APE)\b'
    return t

#----valid track type
def t_TRACKTYPE(t):
    r'\b(AUDIO|CDG|MODE1/2048|MODE1/2352|MODE2/2336|MODE2/2352|CDI/2336|CDI/2352)\b'
    return t

def t_FLAGSVALUE(t):
    r'\b(DCP|4CH|PRE|SCMS)\b'
    return t

#def t_rem_REMKEYWORD(t):
    #r'\b[A-Z_]{4,}\b'
    #return t

def t_REMKEYWORD(t):
    r'\b[A-Z_]{4,}\b'
    return t

# ---- other expected value
def t_TIME(t):
    r'\b\d{2}:\d{2}:\d{2}\b'
    return t

def t_ISRCID(t):
    r'\b[a-zA-Z-0-9]{5}\d{7}\b'
    return t

def t_NUMBER(t):
    r'\b\d{2}\b'
    return t

@TOKEN(value)
def t_VALUE(t):
    t.value = t.value.strip('"')
    return t

# Build the lexer
lexer = lex.lex()

if __name__ == '__main__':

    print datevalue

    # Test it out

    data = u'''
    REM COMMENT ExactAudioCopy v0.99pb4
    REM REPLAYGAIN_TRACK_GAIN -9.59 dB
    REM REPLAYGAIN_TRACK_PEAK 1.000000
    FLAGS DCP
    '''

    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        data = f.read().decode("utf8")

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok


