#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

class CueSheet():

    def __init__(self,
                    catalog   ,
                    cdtextfile,
                    file      ,
                    flags     ,
                    performer ,
                    songwriter,
                    title     ,
                    genre     ,
                    comment   ,
                    date      ,
                    discid    ,
                ):

        self.catalog = catalog
        self.cdtextfile = cdtextfile
        self.file   = file
        self.flags = flags
        self.performer = performer
        self.songwriter = songwriter
        self.title = title
        self.genre = genre
        self.comment = comment
        self.date = date
        self.discid = discid

        pass

    def breakpoints(self):
        pass

    def show(self):
        pass

def createCueSheet( table):

    catalog    = table.get("catalog")
    cdtextfile = table.get("cdtextfile")
    file       = table.get("file")
    flags      = table.get("flags")
    performer  = table.get("performer")
    songwriter = table.get("songwriter")
    title      = table.get("title")

    genre      = table.get("genre")
    comment    = table.get("comment")
    date       = table.get("date")
    discid     = table.get("discid")


    return CueSheet( catalog=catalog,
                     cdtextfile=cdtextfile,
                     file=file,
                     flags=flags ,
                     performer=performer ,
                     songwriter=songwriter,
                     title=title,
                     genre=genre,
                     comment=comment,
                     date=date,
                     discid=discid
                   )



class TrackInfo():
    def __init__(self,
                 title, performer, number, time,
                 isrc, flags, songwriter):

        self.title      = title
        self.performer  = performer
        self.number     = number
        self.time       = time
        self.isrc       = isrc
        self.flags      = flags
        self.songwriter = songwriter

    def __str__(self):

        result = ""

        result += "title: %s, " % (self.title)
        result += "performer: %s, " % (self.performer)
        result += "number: %s, " % (self.number)
        result += "time: %s, " % (self.time)
        result += "isrc: %s, " % (self.isrc)
        result += "flags: %s, " % (self.flags)
        result += "songwriter: %s" % (self.songwriter)

        return result


    def startpoint(self):
        pass

    def debug_repr(self):
        pass


def createTrackInfo( table):

    title      = table.get("title")
    performer  = table.get("performer")
    number     = table.get("number")
    time       = table.get("time")
    isrc       = table.get("isrc")
    flags      = table.get("flags")
    songwriter = table.get("songwriter")

    return TrackInfo( title=title, performer=performer,
                      number=number, time=time,
                      isrc=isrc, flags=flags,
                      songwriter=songwriter
                    )



