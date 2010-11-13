# Copyright 1998-2009 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

__docformat__ = "epytext"

import re

COLOR_MAP_FILE = 'color.map'

havecolor = 1

# Maps style class to tuple of attribute names.
_styles = {}

# Maps attribute name to ansi code.
codes = {}

esc_seq = "\x1b["

codes["normal"]       =  esc_seq + "0m"
codes["reset"]        =  esc_seq + "39;49;00m"

codes["bold"]         =  esc_seq + "01m"
codes["faint"]        =  esc_seq + "02m"
codes["standout"]     =  esc_seq + "03m"
codes["underline"]    =  esc_seq + "04m"
codes["blink"]        =  esc_seq + "05m"
codes["overline"]     =  esc_seq + "06m"
codes["reverse"]      =  esc_seq + "07m"
codes["invisible"]    =  esc_seq + "08m"

codes["no-attr"]      = esc_seq + "22m"
codes["no-standout"]  = esc_seq + "23m"
codes["no-underline"] = esc_seq + "24m"
codes["no-blink"]     = esc_seq + "25m"
codes["no-overline"]  = esc_seq + "26m"
codes["no-reverse"]   = esc_seq + "27m"

codes["bg_black"]      = esc_seq + "40m"
codes["bg_darkred"]    = esc_seq + "41m"
codes["bg_darkgreen"]  = esc_seq + "42m"
codes["bg_brown"]      = esc_seq + "43m"
codes["bg_darkblue"]   = esc_seq + "44m"
codes["bg_purple"]     = esc_seq + "45m"
codes["bg_teal"]       = esc_seq + "46m"
codes["bg_lightgray"]  = esc_seq + "47m"
codes["bg_default"]    = esc_seq + "49m"
codes["bg_darkyellow"] = codes["bg_brown"]

def color(fg, bg="default", attr=["normal"]):
    mystr = codes[fg]
    for x in [bg]+attr:
        mystr += codes[x]
    return mystr


ansi_codes = []
for x in range(30, 38):
    ansi_codes.append("%im" % x)
    ansi_codes.append("%i;01m" % x)

rgb_ansi_colors = ['0x000000', '0x555555', '0xAA0000', '0xFF5555', '0x00AA00',
    '0x55FF55', '0xAA5500', '0xFFFF55', '0x0000AA', '0x5555FF', '0xAA00AA',
    '0xFF55FF', '0x00AAAA', '0x55FFFF', '0xAAAAAA', '0xFFFFFF']

for x in range(len(rgb_ansi_colors)):
    codes[rgb_ansi_colors[x]] = esc_seq + ansi_codes[x]

del x

codes["black"]     = codes["0x000000"]
codes["darkgray"]  = codes["0x555555"]

codes["red"]       = codes["0xFF5555"]
codes["darkred"]   = codes["0xAA0000"]

codes["green"]     = codes["0x55FF55"]
codes["darkgreen"] = codes["0x00AA00"]

codes["yellow"]    = codes["0xFFFF55"]
codes["brown"]     = codes["0xAA5500"]

codes["blue"]      = codes["0x5555FF"]
codes["darkblue"]  = codes["0x0000AA"]

codes["fuchsia"]   = codes["0xFF55FF"]
codes["purple"]    = codes["0xAA00AA"]

codes["turquoise"] = codes["0x55FFFF"]
codes["teal"]      = codes["0x00AAAA"]

codes["white"]     = codes["0xFFFFFF"]
codes["lightgray"] = codes["0xAAAAAA"]

codes["darkteal"]   = codes["turquoise"]
# Some terminals have darkyellow instead of brown.
codes["0xAAAA00"]   = codes["brown"]
codes["darkyellow"] = codes["0xAAAA00"]



# Colors from /etc/init.d/functions.sh
_styles["NORMAL"]     = ( "normal", )
_styles["GOOD"]       = ( "green", )
_styles["WARN"]       = ( "yellow", )
_styles["BAD"]        = ( "red", )
_styles["HILITE"]     = ( "teal", )
_styles["BRACKET"]    = ( "blue", )

# Portage functions
_styles["INFORM"]                  = ( "darkgreen", )
_styles["UNMERGE_WARN"]            = ( "red", )
_styles["SECURITY_WARN"]           = ( "red", )
_styles["MERGE_LIST_PROGRESS"]     = ( "yellow", )
_styles["PKG_BLOCKER"]             = ( "red", )
_styles["PKG_BLOCKER_SATISFIED"]   = ( "darkblue", )
_styles["PKG_MERGE"]               = ( "darkgreen", )
_styles["PKG_MERGE_SYSTEM"]        = ( "darkgreen", )
_styles["PKG_MERGE_WORLD"]         = ( "green", )
_styles["PKG_BINARY_MERGE"]        = ( "purple", )
_styles["PKG_BINARY_MERGE_SYSTEM"] = ( "purple", )
_styles["PKG_BINARY_MERGE_WORLD"]  = ( "fuchsia", )
_styles["PKG_UNINSTALL"]           = ( "red", )
_styles["PKG_NOMERGE"]             = ( "darkblue", )
_styles["PKG_NOMERGE_SYSTEM"]      = ( "darkblue", )
_styles["PKG_NOMERGE_WORLD"]       = ( "blue", )
_styles["PROMPT_CHOICE_DEFAULT"]   = ( "green", )
_styles["PROMPT_CHOICE_OTHER"]     = ( "red", )

def nc_len(mystr):
    tmp = re.sub(esc_seq + "^m]+m", "", mystr);
    return len(tmp)

def nocolor():
    "turn off colorization"
    global havecolor
    havecolor = 0

def resetColor():
    return codes["reset"]

def style_to_ansi_code(style):
    """
    @param style: A style name
    @type style: String
    @rtype: String
    @return: A string containing one or more ansi escape codes that are
        used to render the given style.
    """
    ret = ""
    for attr_name in _styles[style]:
        # allow stuff that has found it's way through ansi_code_pattern
        ret += codes.get(attr_name, attr_name)
    return ret

def colorize(color_key, text):
    global havecolor
    if havecolor:
        if color_key in codes:
            return codes[color_key] + text + codes["reset"]
        elif color_key in _styles:
            return style_to_ansi_code(color_key) + text + codes["reset"]
        else:
            return text
    else:
        return text


def create_color_func(color_key):
    def derived_func(*args):
        newargs = list(args)
        newargs.insert(0, color_key)
        return colorize(*newargs)
    return derived_func

compat_functions_colors = ["bold", "white", "teal", "turquoise", "darkteal",
    "fuchsia", "purple", "blue", "darkblue", "green", "darkgreen", "yellow",
    "brown", "darkyellow", "red", "darkred"]

#for c in compat_functions_colors:
    #globals()[c] = create_color_func(c)

for c in codes.keys():
    globals()[c] = create_color_func(c)




