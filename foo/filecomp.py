#! /usr/bin/env python
# -*- coding: utf-8 -*-

## filecomp.py, comparing files
##     Copyright (C) 2012 Angel Luis Garcia Garcia
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Constants.

CASE_SENSITIVE = True
VERSION = '0.0.1'
SCRIPTNAME = 'filecomp.py'

# Modules.

import os
import zipfile
import sys

# Classes.

class Container(object):
    '''
    Class container. 
    A container should be a directory, zip file or a regular file.
    '''
    def __init__(self, path):
        '''Constructor code'''
        # Attributes.
        self.__path = path
        self.__type = None
        # Detect the container.
        self.__detectContainer()

    def __detectContainer(self):
        '''Detect container'''
        # Directory?
        if os.path.isdir(self.__path):
            self.__type = 'd'
        # File?
        if os.path.isfile(self.__path):
            # Is zip file?
            if zipfile.is_zipfile(self.__path):
                self.__type = 'z'
            else: self.__type = 'f'

    def containerExists(self):
        return False if self.__type is None else True

    def getFiles(self):
        '''Return list of files'''
        if self.__type in ['f']: 
            a = os.path.split(self.__path)
            return [(a[1], a[0])]
        if self.__type in ['d']:
            # Walking directory.
            a = os.walk(self.__path) # Returns a generator.
            aux = list()
            while True:
                try:
                    b = a.next()
                    dirpath = b[0]
                    filenames = b[2:]
                    for i in filenames:
                        for j in i: aux.append((j, dirpath))
                except:
                    break
            return aux
        if self.__type in ['z']:
            a = zipfile.ZipFile(self.__path,"r")
            aux = list()
            for i in a.namelist():
                a = os.path.split(i)
                if len(a[1]) == 0: continue # It's a directory.
                aux.append((a[1], a[0]))
            return aux

    def compareFiles(self, A, B, case_sensitive = True):
        '''Returns files in A but not in B with options'''
        for i in A:
            nfileA = i[0]
            pathA = i[1]
            drWatson = True
            for j in B:
                nfileB = j[0]
                if not case_sensitive: aux = nfileA.lower().strip() == nfileB.lower().strip()
                else: aux = nfileA.strip() == nfileB.strip()
                if aux: 
                    drWatson = False
                    break
            if drWatson: print "File: %s (%s)" % (nfileA, pathA)

# Functions.

def f_help():
    text = '''
    %s %s

    Execute: filecomp.py Source Target

    This program returns files in Source but not in Target,
    where Source and Target could be a directory, file or
    zip file.

    This script runs with Python 2.6/2.7 in Linux and Windows.
    Written by Angel Luis Garcia Garcia (angelluis78@gmail.com).
    License: GNU GPL v3.
    ''' % (SCRIPTNAME, VERSION)
    print text

# Script.

if len(sys.argv[1:]) == 2:
    fileA = sys.argv[1]
    fileB = sys.argv[2]
else:    
    f_help()
    sys.exit(0)

source = Container(fileA)
target = Container(fileB)

if not source.containerExists():
    print "Source %s not exists" % (fileA)
    sys.exit(0)

if not target.containerExists():
    print "Target %s not exists" % (fileB)
    sys.exit(0)

print "Searching files that are in %s but not in %s ..." % (fileA, fileB)    
source.compareFiles(source.getFiles(), target.getFiles(), CASE_SENSITIVE)
