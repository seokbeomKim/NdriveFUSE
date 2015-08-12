#!/usr/bin/env python
# coding=utf-8
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

confgen.py

This file implements 'ConfGenerator' class which uses AES encryption and 
decryption to handle user's account information. 
"""
from Crypto.Cipher import AES
from Crypto import Random
from getpass import getpass

import re
import os
import sys
import base64

class ConfGenerator(object):
    ####################
    # Flag for debugging
    ####################
    debug = False

    # configuration members
    id = ""
    pw = ""

    #####################################
    # Member variables for AES encryption
    #####################################
    #
    # Configuration file information
    FILE_PATH = os.getenv("HOME") + "/.ndrivecfg"
    BLOCK_SIZE = 32
    PADDING = '{'
    pad = lambda self, s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * self.PADDING
    # one-liners to encrypt/encode and decrypt/decode a string
    # encrypt with AES, encode with base64
    EncodeAES = lambda self, c, s: base64.b64encode(c.encrypt(self.pad(s)))
    DecodeAES = lambda self, c, e: c.decrypt(base64.b64decode(e)).rstrip(self.PADDING)
    #
    # generate a random secret key
    secret = os.urandom(BLOCK_SIZE)
    #
    # create a cipher object using the random secret
    cipher = AES.new(secret)
    ################################################

    """
    __init__(self, debug = False)
    """
    def __init__(self, debug = False):
        self.debug = debug
        if (debug == True):
            print("**__init__** ConfGenerator instance is initialized.")

    """
    readConfFile(self)
    
    Read configuration file and read cutomized values
    1. Account information: id, pw, key
    2. Cache
    - Filesize limit
    - File type
    - Directories
    - files
    """
    def readConfFile(self):
        if (self.debug == True):
            print("**readConfFile** try to read configuration file.")

        try:
            confFile = open(self.FILE_PATH, 'r')
        except:
            print "Please make configuration file. See the instruction https://github.com/seokbeomKim/NdriveFUSE"
            sys.exit(1)

        read = confFile.readlines()
        for item in read:
            # Pass comment or empty string
            if not item.strip() or item[0] is '#':
                continue
            
            i = re.split('([\w]+)([\= ]+)(.*)', item)
            # i[2] is encypted string
            r = i[3]


            if i[1] == "id":
                self.id = r
            elif i[1] == "pw":
                self.pw = r
            elif i[1] == "key":
                # Set the AES key
                read = re.split('([\= ]+)(.*)', item)
                self.secret = read[2]
                self.cipher = AES.new(self.secret)

            else:
                r = re.sub('[\"\']', '', r)
                if i[1] == "cache_exclude_filesize":
                    self.cache_exclude_filesize = int(r)
                    continue
                elif i[1] == "cache_directory":
                    self.cache_directory = r
                    continue
                elif i[1] == "cache_exclude_filetype":
                    r = re.split('[,\ ]?([\w]+)[,\ ]?', r)
                    r = filter(None, r)
                    self.cache_exclude_filetype = r
                    continue
                    
                r = re.split('([\w\/]+)[, ]+([\w\/]+)', r)
                r = filter(None, r)                
                if i[1] == "cache_exclude_directories":
                    self.cache_exclude_directories = r
                elif i[1] == "cache_exclude_files":
                    self.cache_exclude_files = r
                
        self.id = self.DecodeAES(self.cipher, self.id)
        self.pw = self.DecodeAES(self.cipher, self.pw)
        return self.id, self.pw

    """
    getAccountInfo()
    """
    def getAccountInfo(self):
        return self.id, self.pw

    """
    generateFile()
    
    To generate id, pw, key and put them into configuration file.
    """
    def generateFile(self):
        # Print short notice about this script
        print('This script will generate config file in path (' + self.FILE_PATH + ') with encrypted your account name and password information. If you want to change the config file, please re-run this script file. It will change your config file with new account information.')
        
        # Get user input (y or n only)
        while True:
            answer = raw_input("Okay, I understand. Choice: (Y/N) ")
            answer = answer.lower()
            
            if (answer[0] == "n") or (answer[0] == "y"):
                break
            else:
                print("Please input y or n")
                
        if answer == "n":
            print("Please read the notice above.")
            sys.exit(0)
                    
                    
        # If the user input YES, get user's input for account setting
        id = raw_input("Enter your naver account name: ")
        id = id.strip()
        
        pw = getpass("Enter the password: ")
        pw = pw.strip()
        
        # Encrypt account name and password
        print("id = " + id + ", pw = " + pw)
        id = self.EncodeAES(self.cipher, id)
        pw = self.EncodeAES(self.cipher, pw)
        
        # Store encrypted information to configuration file
        configFile = open(self.FILE_PATH, "a+")
        configFile.write("key = " + self.secret + os.linesep)
        configFile.write("id = " + id + os.linesep)
        configFile.write("pw = " + pw + os.linesep)
        configFile.close()
        sys.exit(0)
    
