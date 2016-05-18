#!/usr/bin/env python
"""
Copyright 2015-2016 Sukbeom Kim

This file is part of NdriveFuse (https://github.com/seokbeomKim/NdriveFUSE/)

NdriveFUSE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
any later version.

NdriveFUSE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with NdriveFUSE.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Author: Sukbeom Kim
E-mail: chaoxifer@gmail.com

helper.py

Implements wrapper functions.

This source includes several functions used for wrapper function (between ndrive 
and fuse). To be specific, those functions could be:

* Convert from date string to time tick
* Check file (attributes, path)

"""

import re
import pdb
import time
import datetime
import sqlite3
import os
import sys

"""
[Name]
converToDateToClock(date)

[Description]
convert from date string to time clock
- date: return value from ndrive library. The format is "2015-07-09T11:11:29+09:00".

[NOTES]
Using regular expression, the function devide the string into two parts (date + time).
With the information from the values, make time structure to use 'time.mktime(t)'. The
return value from mktime would be used in getattr to represent ctime, atime, and mtime.
"""
def convertDateToTick(date):
#    print "**converDateToTick**" + date
    s_date = re.split('([\w+\-]*)T(.*)', date)

    # s_data[1] would be "yyyy-mm-dd": represents date
    # s_data[2] would be "hh:mm:ss+xx:xx": represents time
    rdate = re.findall('([\w]+)', s_date[1])
    rtime = re.findall('([\w]+)', s_date[2])

    # We need to figure DOW out
    date_obj = datetime.date(int(rdate[0]), int(rdate[1]), int(rdate[2]))

    # Not sure about last element: isdst
    # If there's problem in the future, timezone has to be checked later.
    rValue = (int(rdate[0]), int(rdate[1]), int(rdate[2]), \
              int(rtime[0]), int(rtime[1]), int(rtime[3]), \
              int(date_obj.weekday()), int(date_obj.strftime('%j')), 0)

    return time.mktime(rValue)

# End of convertDataToTick(date)

"""
[Name]
checkItemFromOtherList(item, list)

[Description]
To check whether the same item(:item) exists in the list(:list)

[NOTES]
If item is in the list, the return value will be True. Otherwise, return value
will be False.

"""
def checkItemFromOtherList(item, list):
    item = re.sub('\ ','', item)
    for compareTo in list:
        compareTo = re.sub('\ ','', compareTo)
        if compareTo == item:
            return True
    return False

def checkFileFromDirectoryList(filepath, dirlist):
    for dirpath in dirlist:
        dirpath = re.sub('\ ','', dirpath)
        if filepath[:len(dirpath)] == dirpath:
            return True
    return False

class DatabaseManager(object):
    def __init__(self):
        #print "Database manager initialized..."
        self.db_path = os.path.join(os.getenv('HOME'), '.ndrive.db')
        self.cursor = None
        self.con = None
        
    def checkDatabaseFile(self):
        return os.path.isfile(self.db_path)
        
    def connect(self):
        self.con = sqlite3.connect(self.db_path)
        self.cursor = self.con.cursor()
    
    def initialize(self):
        #print "Create new database file..."
        self.cursor.execute(
            "CREATE TABLE FILE_TABLE(file_href text UNIQUE, creationdate text, getcontentlength text, getlastmodified text, lastaccessed text, resourceno text, resourcetype text)")
        self.con.commit()
        
    def registerFile(self, target):
        #print "Register file information to database..."
        try:
            self.cursor.execute(
                "INSERT INTO FILE_TABLE(file_href, creationdate, getcontentlength, getlastmodified, lastaccessed, resourceno, resourcetype)\
                VALUES(?, ?, ?, ?, ? ,? ,?)", (target['href'], target['creationdate'], target['getcontentlength'], target['getlastmodified'], target['lastaccessed'], target['resourceno'], target['resourcetype'] )
            )
            self.con.commit()
        except:
            self.removeFile(target)
            self.cursor.execute(
                "INSERT INTO FILE_TABLE(file_href, creationdate, getcontentlength, getlastmodified, lastaccessed, resourceno, resourcetype)\
                VALUES(?, ?, ?, ?, ? ,? ,?)", (target['href'], target['creationdate'], target['getcontentlength'], target['getlastmodified'], target['lastaccessed'], target['resourceno'], target['resourcetype'] )
            )
            self.con.commit()
    def updateFile(self, target):
        #print "Update file information..."
        self.cursor.execute(
            "UPDATE FILE_TABLE SET file_href='%s', creationdate='%s', getcontentlength='%s', getlastmodified='%s', lastaccessed='%s', resourceno='%s', resourcetype='%s' WHERE file_href = '%s'",
            (target['href'], target['creationdate'], target['getcontentlength'], target['getlastmodified'], target['lastaccessed'], target['resourceno'], target['resourcetype'],target['href'] )
        )
        self.con.commit()
        
    def removeFile(self, target):
        #print "Remove file information..."
        self.cursor.execute(
            "DELETE FROM FILE_TABLE WHERE file_href='"+target['href']+"'"
        )
        self.con.commit()
    
    def removeFileWithPath(self, old):
        #print "Update file information (reason: rename)..."
        self.cursor.execute(
            "DELETE FROM FILE_TABLE WHERE file_href='"+old+"'"
        )
        self.con.commit()
    def uploadFile(self, target):
        #print target
        #print "Update file information (reason: upload)..."
        try:
            self.removeFile(target)
        except:
            pass
        
        try:
            self.registerFile(target)
        except:
            pass
    def disconnect(self):
        self.con.close()
        
    def getTimeStamp(self, file_href):
        self.cursor.execute(
            "SELECT getlastmodified FROM FILE_TABLE WHERE file_href = '" + file_href + "'")
        rv = self.cursor.fetchone()
        return rv[0]
        
        