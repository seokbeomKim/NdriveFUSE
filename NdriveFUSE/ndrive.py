#!/usr/bin/env python
# coding=utf-8
from __future__ import with_statement

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

# ======
# Notice
# ======
# NDriveFUSE
# author: Sukbeom Kim(chaoxifer@gmail.com)

"""
NDriveFUSE uses ndrive python wrapper project (https://github.com/carpedm20/ndrive).
Thanks to carpedm20's help to finish this project.
"""
# If you have an issue or want to contribute with bug report, please mail to me.


# =========
# Important
# =========
# Conflict between fusepy and python2-fuse
#
# There are two libraries written in python for using FUSE. Both of them have same file
# (/usr/lib/python2.x/site-packages/fuse.py). Therefore, user has to resolve the
# conflict between 'fusepy' and 'python2-fuse'. For this NDriveFUSE, you need to
# install fusepy instead of python2-fuse

from errno import *
import os
import ntpath
import sys
import errno
import cmd
import locale
from os.path import expanduser
import pprint
import shlex
import time
from datetime import date
import getpass
import pdb
from clint.textui import colored
from ndrive import Ndrive
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))
sys.path.append(os.path.join(os.path.dirname(__file__), "ndrive"))

import fuse
import confgen
import ndrive
import webbrowser
import stat
from helper import *
import threading

class NDriveFUSE(Operations):
    def __init__(self, root, id, pw, confMgr):
        #sys.setdefaultencoding('utf-8')
        print "Sync destination directory = " + root
        
        self.confMgr = confMgr
        self.root = root # mountpoint
        self.ndrive = Ndrive()
        self.id = id
        self.pw = pw
        self.cache = []
        self.dbMgr = DatabaseManager()
        

        r = self.ndrive.login(self.id, self.pw)
        if r:
            print "Succeed to sign in: " + id + "\n"
        else:
            print "Failed to sign in. Check your connection or configuration."
            
        if self.dbMgr.checkDatabaseFile() == False:
            #print "No database. Create new one..."
            self.dbMgr.connect()
            self.dbMgr.initialize()

        else:
            self.dbMgr.connect()

        self.Sync()
        self.initStat()
        self.looper()

    def Sync(self, path="/"):
        print "Start syncing..."
        if not os.path.isdir(self.confMgr.cache_directory):
            os.mkdir(self.confMgr.cache_directory, 0755)

        allFiles = self.ndrive.getListOfAllFiles(path)
        allFiles_result = [] # This is list of filtered files
        
        # Exclude files from list in config file.
        for idx, item in enumerate(allFiles):
            flag = False
            # 1) directory
            if item['resourcetype'] == "collection":
                if checkItemFromOtherList(item['href'], self.confMgr.cache_exclude_directories) == True:
                    flag = True
                item_path = re.split('[\/]?([\w]+)[\/]?', item['href'])
                item_path = filter(None, item_path)
                for directory in self.confMgr.cache_exclude_directories:
                    try:
                        excluded_path = re.split('[\/]?([\w]+)[\/]?', directory)
                        excluded_path = filter(None, excluded_path)
                        for i, y in enumerate(excluded_path):
                            if y == item_path[i]:
                                flag = True
                                break
                        if flag == True:
                            break
                    except:
#                        print "FAIL to split path with item_path = " + item['href'] + ", directory = " + directory
                        continue             
            # 2) regular file
            else:
                if checkFileFromDirectoryList(item['href'], 
                                              self.confMgr.cache_exclude_files) or \
                checkItemFromOtherList(re.sub('[\ \.]','',
                                              os.path.splitext(item['hilightfilename'])[1]),
                                       self.confMgr.cache_exclude_filetype) or \
                int(item['getcontentlength']) / 1024 > int(self.confMgr.cache_exclude_filesize):
                    flag = True

            if flag == False:
                allFiles_result.append(item)
                
        # print allFiles_result

        message = "Number of filtered files: " + str(len(allFiles_result))
        print message

        local_file_lists = os.listdir(self.confMgr.cache_directory)
        # Sync the files
        for idx, file in enumerate(allFiles_result):
            fpath = self.confMgr.cache_directory + file['href']
            # directory
            if file['resourcetype'] == "collection":
                try:
                    dpath = self.confMgr.cache_directory + file['href']
                    os.mkdir(dpath, 0755)
                except:
                    pass 
            # file
            else:
                try:
                    if os.path.isfile(fpath):
                        print "File exist. check file's timestamp."
                        if self.compareTimeStamp(file['getlastmodified'],
                                            self.dbMgr.getTimeStamp(file['href'])):
                            self.ndrive.downloadFile(file['href'], fpath)
                            print "File downloaded"
                            self.dbMgr.updateFile(file)
                            
                    else:
                        print "Download file"
                        self.dbMgr.registerFile(file)
                        self.ndrive.downloadFile(file['href'], fpath)

                except Exception, e:
                    print "Exception occured while syncing files..." , e
                    pass
        return
    
    
    
    ########################################################
    # Fuse functions
    ########################################################

    """
    compareTimeStamp(self)
    
    check timestamp to decide whether new file exists or not.
    date1이 date2보다 최신일 경우에 True, 아닌 경우에는 False 반환
    
    이 때 파라미터 형식은 '2015-08-09T18:10:07+09:00'
    """
    def compareTimeStamp(self, date1, date2):
        s_date1 = re.split('([\w+\-]*)T(.*)', date1)
        rdate1 = re.findall('([\w]+)', s_date1[1])
        rtime1 = re.findall('([\w]+)', s_date1[2])
        d = datetime.date(int(rdate1[0]), int(rdate1[1]), int(rdate1[2]))
        t = datetime.time(int(rtime1[0]), int(rtime1[1]))
        ts1 = datetime.datetime.combine(d, t)
        
        s_date2 = re.split('([\w+\-]*)T(.*)', date2)
        rdate2 = re.findall('([\w]+)', s_date2[1])
        rtime2 = re.findall('([\w]+)', s_date2[2])
        d = datetime.date(int(rdate2[0]), int(rdate2[1]), int(rdate2[2]))
        t = datetime.time(int(rtime2[0]), int(rtime2[1]))
        ts2 = datetime.datetime.combine(d, t)
        
        if not ts1 < ts2:
            # need synchronization
#            print "Need to sync."
            return True
        else:
#            print "Doesn't need to sync."
            return False
    """
    getFullPath(self, path)
    - path: parameter to get full path with self.current_path
    """
    def getFullPath(self, path):
#        path = os.path.join('/', path)
        path = self.confMgr.cache_directory + path
        return path

    def getRelativePath(self, path):
        path = re.sub(self.confMgr.cache_directory,'', path)
        return path
    """
    isUnconsequentialFiles(self, name)
    - name: file name

    Due to gvfs, those files in unconsequential list would be created automatically. 
    It has to be handled when FUSE trys to get entries from a directory. In that case,
    ENOENT will be returned. (:139 line)
    """
    def isUnconsequentialFiles(self, name):
        unconsequential = ['Thumbs.db', '.DS_STORE', '.Trash', '.Trash-1000',
                           '.xdg-volume-info', '.directory', 'autorun.inf',
                           'AACS', 'BDSVM', 'BDMV']
        if name in unconsequential:
            return True
        else:
            return False

    """
    isDirectory(self, path)
    - path: file path
    """
    def isDirectory(self, path):
        if path == '/':
            return True
        
        for entry in self.cache:
            name = entry[:-1]
            if name == path:
                return True
        return False

    def access(self, path, mode):
        full_path = self.getFullPath(path)
        
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)
    
    def chmod(self, path, mode):
        full_path = self.getFullPath(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self.getFullPath(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh):
        """
        write후에 getattr이 호출되므로 timestamp를 비교하여 업로드 여부를 판단한다.
        """
        full_path = self.getFullPath(path)
        st = os.lstat(full_path)
        r = dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

        return r        

    """
    readdir(self, path, fh)
    
    To make sure 'readdir' function properly, we need to subtract '/' character from
    entries in directory. (In other words, all of entries have to have name without 
    character '/'
    """
    def readdir(self, path, fh):
        full_path = self.getFullPath(path)
        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        return dirents

    def readlink(self, path):
        return 0

    """
    insertToDirCache(self, path)

    From Ndrive().getList(), the directory has name in format ("dirname/"). We need to 
    remove '/' character for readdir() but to know which file is directory. To know that,
    we use direntry cache. When readdir() get entry list from current path, it calls this 
    function and save only directory information into the cache.
    """
    def insertToDirCache(self, path):
        if path[len(path)-1] == '/':
            if path not in self.cache:
                self.cache.append(path)
    
    """
    mknod
    Create a file node

    This is called for creation of all non-directory, non-symlink nodes. If the filesystem defines a create() method, then for regular files that will be called instead.
    """
    def mknod(self, path, mode, dev):
        rValue = os.mknod(self.getFullPath(path), mode, dev)
        return rValue

    def rmdir(self, path):
        full_path = self.getFullPath(path)
        self.ndrive.delete(path + "/")
        # self.dbMgr.removeDirectory(path)        
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        self.ndrive.makeDirectory(path)
        return os.mkdir(self.getFullPath(path), mode)

    def statfs(self, path):
        full_path = self.getFullPath(path)
        full_path = unicode(full_path).encode("utf-8")
        
        stv = os.statvfs(full_path)
        rValue = dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

        rValue['f_blocks'] = self.statinfo['f_blocks']
        return rValue

    """
    initStat()
    
    df와 nautilus같은 파일 매니저에서 보여질 디스크 정보를 초기화한다.
    """
    def initStat(self):
        disk_info = self.ndrive.getDiskSpace()
        
        totalspace  = disk_info['totalspace']
        unusedspace = disk_info['unusedspace']
        f_frsize = 4096
        f_blocks = totalspace / f_frsize
        f_bfree = unusedspace / f_frsize
                
        rValue = {'f_bavail':4096,
                  'f_bfree':f_bfree,   # Total number of free blocks in -
                  'f_blocks':f_blocks,  # Total number of blocks in the file system
                  'f_bsize':f_frsize,       # preferred block size
                  'f_favail':9023386, # Free nodes available to non-super user.
                  'f_ffree':9023386, # Total number of free file nodes.
                  'f_files':10231808, # Total number of file nodes.
                  'f_flag':4096, # Flags. System dependent: see statvfs() man page.
                  'f_frsize':4096,      # fundamental file system block size
                  'f_namemax':255
                  }
        self.statinfo = rValue

    def unlink(self, path):
        self.ndrive.delete(path)
        return os.unlink(self.getFullPath(path))        

    def symlink(self, name, target):
        return 0

    def rename(self, old, new):
        print old, new
        self.ndrive.uploadFile(self.getFullPath(old), new, True)
        self.ndrive.delete(old)
        self.dbMgr.removeFileWithPath(old)
        self.dbMgr.registerFile(self.ndrive.getProperty(new))
        
        return os.rename(self.getFullPath(old), self.getFullPath(new))

    def link(self, target, name):
        return 0

    def utimens(self, path, times=None):
        return os.utime(self.getFullPath(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self.getFullPath(path)
        return os.open(full_path, flags)
        
    def create(self, path, mode, fi=None):
        full_path = self.getFullPath(path)

        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)
        
    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self.getFullPath(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        try:
            local_file_timestamp = self.dbMgr.getTimeStamp(path)
            mtime = os.path.getmtime(self.getFullPath(path))
            m_date = datetime.datetime.fromtimestamp(mtime)
            compareStr = m_date.strftime("%Y-%m-%dT%H:%M+09:00")
            # print compareStr + ", " + local_file_timestamp
            if not self.compareTimeStamp(compareStr, local_file_timestamp):
                self.ndrive.uploadFile(self.getFullPath(path), path, True)
                self.dbMgr.uploadFile(self.ndrive.getProperty(path))
        except:
            self.ndrive.uploadFile(self.getFullPath(path), path, True)
            self.dbMgr.uploadFile(self.ndrive.getProperty(path))

        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)

    """
    recoverSession:

    Keep user's session from being timeout
    """
    def recoverSession(self):
        #print "Refresh session..."
        self.ndrive.getDiskSpace()
        time.sleep(1)

    def looper(self):
        # Thread to keep session
        try:
            self.recover = threading.Timer(10, self.looper)
            self.recover.start()
            self.Sync()
        except (KeyboardInterrupt, SystemExit):
            print "Exit the program."
            sys.exit()
            
        self.recoverSession()
    
def main(mountpoint):
    confMgr = confgen.ConfGenerator()
    confMgr.readConfFile()
    account = confMgr.getAccountInfo()
    obj = NDriveFUSE(mountpoint, account[0], account[1], confMgr)
    FUSE(obj, mountpoint, nothreads=True, foreground=True)
    obj.recover.cancel()
    sys.exit(0)
    
if __name__ == '__main__':
    main(sys.argv[1])
