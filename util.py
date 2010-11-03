#!/usr/bin/env python
# vim: set fileencoding=utf-8 :


def infomsg (text):
    print (text)

def strip(text):
    """
        strip leading & trailing whitespaces, single/double quotes
    """

    return text.strip().strip("'").strip('"')

