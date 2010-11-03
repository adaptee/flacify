#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

supported_exts = [
                    '.ape' , '.APE' ,
                    '.flac', '.FLAC',
                    '.tta' , '.TTA' ,
                    '.wv'  , '.WV'  ,
                    '.wav' , '.WAV' ,
                 ]

ext2decoder    = {
                    ".ape"  : "mac",
                    ".flac" : "flac",
                    ".tta"  : "ttaenc",
                    ".wv"   : "wvunpack",
                 }



def infomsg (text):
    print (text)

def strip(text):
    """
        strip leading & trailing whitespaces, single/double quotes
    """

    return text.strip().strip("'").strip('"')

