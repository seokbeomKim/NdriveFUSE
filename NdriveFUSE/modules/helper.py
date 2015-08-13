#!/usr/bin/env python
"""
Copyright 2015 Sukbeom Kim

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
        print "**checkFileFromDirectoryList** filepath = "+filepath+" is compared to "+dirpath[:len(filepath)]
        if filepath[:len(dirpath)] == dirpath:
            return True
    return False

