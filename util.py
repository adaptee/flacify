#!/usr/bin/env python
# vim: set fileencoding=utf-8 :


from color import green

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
                    ".wav"  : "ls",  # tricky, wav does need decoder!
                 }



def infomsg (text):
    print green(text)
    #print text

def strip(text):
    """
        strip leading & trailing whitespaces, single/double quotes
    """

    return text.strip().strip("'").strip('"')

