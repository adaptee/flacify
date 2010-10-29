#!/usr/bin/env python
# vim: set fileencoding=utf-8 :


def get(table, key):
    return table.get(key, "")

class CueSheet(object):

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
                    tracks    ,
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

        self.tracks = tracks

    def showbreakpoints(self):

        breakpoints = ""

        # carefully skip the first track
        for track in self.tracks[1:]:
            breakpoints += "%s\n" % (track.startpoint(), )

        return breakpoints


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

    tracks     = table.get("tracks")

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
                     discid=discid,
                     tracks=tracks
                   )

class TrackInfo(object):
    def __init__(self,
                 title, performer, number, offset,
                 isrc, flags, songwriter):

        self.title      = title
        self.performer  = performer
        self.number     = number
        self.offset     = offset
        self.isrc       = isrc
        self.flags      = flags
        self.songwriter = songwriter

    #def __init__(self, table):
        #self.title      = table.get("title", "")
        #self.performer  = table.get("performer", "")
        #self.number     = table.get("number", "")
        #self.offset     = table.get("offset", "")
        #self.isrc       = table.get("isrc", "")
        #self.flags      = table.get("flags", "")
        #self.songwriter = table.get("songwriter", "")

        #self.artist = self.performer



    def __str__(self):

        result = ""

        result += "title: %s, " % (self.title)
        result += "performer: %s, " % (self.performer)
        result += "number: %s, " % (self.number)
        result += "offset: %s, " % (self.offset)
        result += "isrc: %s, " % (self.isrc)
        result += "flags: %s, " % (self.flags)
        result += "songwriter: %s" % (self.songwriter)

        return result

    def startpoint(self):
        return self.offset

    def debug_repr(self):
        pass


def createTrackInfo( table):

    #return TrackInfo(table)


    title      = table.get("title")
    performer  = table.get("performer")
    number     = table.get("number")
    offset       = table.get("offset01")
    isrc       = table.get("isrc")
    flags      = table.get("flags")
    songwriter = table.get("songwriter")

    #print "offset: %s " % (offset,)

    return TrackInfo( title=title, performer=performer,
                      number=number, offset=offset,
                      isrc=isrc, flags=flags,
                      songwriter=songwriter
                    )



