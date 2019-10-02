#!/usr/bin/env python

# mp3toogg.py
# an MP3 to OGG converter
# Copyright (C) 2007 C. Jayakumar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Place this script in your Music directory. This script will go through 
# your Music directory and all the subdirectories that exist under the main 
# Music directory, and will convert all the MP3 files that exist to OGG files.
# It uses the 'commands' python module, which is Unix-specific.
# 
# what you need to have:
#     mpg321
#     oggenc (part of vorbis-tools)
#     python 2.5
# 
# how to run the script (two ways)
#     run 'python mp3toogg.py', or
#     a. make the script executable - chmod +x mp3toogg.py
#     b. execute the script - ./mp3toogg.py
# 
# Caveats
#     your MP3 files MUST have a LOWER-CASE extension, ie. mp3, NOT Mp3 or MP3 or mP3(?)
#     your MP3 files MUST be named ONLY with the extension .mp3, NOT .mpeg3
#     .mp3, .mp3, that's the only extension allowed.
#     NO DOUBLE-QUOTES in the filename. please convert double-quotes to single-quotes. 
#        For example, convert "Oran "Juice" Jones - The Rain.mp3" to "Oran 'Juice' Jones
#         - The Rain.mp3"
#     the script creates and uses an intermediate file called 'mp3tooggintermediatewav'. 
#        hopefully, you will not have or need a file with the same name in your Music directory.
#     these are the only reasons that I've seen so far for the script not working or 
#        misbehaving. If you find anything more, please email me. (Or better yet, please 
#        change the script yourself and let me know.)
# 
# how it works
#     it traverses the directory tree looking for MP3 files
#     when it finds a file, it executes 'mpg321 'filename.mp3' -w mp3tooggintermediatewav'. 
#        this converts the MP3 file to an uncompressed WAV format
#     then it executes 'oggenc mp3tooggintermediatewav -o 'filename.ogg'. this converts 
#        the uncompressed WAV format to an OGG file.
#     then, 'rm mp3tooggintermediatewav'. this removes the intermediate file.
#     if all of the above succeeds, then 'rm filename.mp3'. this removes the MP3 file.
#     a log file, 'mp3toogg.log' will be created in same directory that the script is run 
#        from. This log file contains the output from all the above shell command executions.

import os
import commands
import fnmatch


def convertallmp3stoogg(currdir, logfile):
    '''
    this converts all the mp3s to oggs in the current directory and all
    subdirectories recursively.
    '''
    # walk each individual directory and perform the conversion
    for root, dirs, files in os.walk(currdir):
        # list of qualified mp3 filenames
        qualifiedfiles = []

        # if the file is an mp3 file, qualify it and add it to the list
        for filename in files:
            if fnmatch.fnmatch(filename, '*.mp3'):
                filename = os.path.join(root, filename)
                qualifiedfiles.append(filename)

        # convert each mp3 file to an ogg file
        for mp3file in qualifiedfiles:
            print "Processing file: " + mp3file
            print >> logfile, "mp3toogg.py: Processing file - " + mp3file
            convertmp3toogg(mp3file, logfile)


def convertmp3toogg(mp3file, logfile):
    '''
    this takes an mp3 file and converts it to an ogg file
    '''
    # split the filename and extension
    (nomp3filename, ext) = os.path.splitext(mp3file)

    # decode the mp3 into a raw wave format
    cmd = 'mpg321 "' + mp3file + '" -w mp3tooggintermediatewav'
    (mp3status, mp3output) = commands.getstatusoutput(cmd)
    outputtologfile(logfile, mp3status, mp3output)

    # encode the raw wave format to an ogg file
    cmd = 'oggenc mp3tooggintermediatewav -o "' + nomp3filename + '.ogg"'
    (oggstatus, oggoutput) = commands.getstatusoutput(cmd)
    outputtologfile(logfile, oggstatus, oggoutput)

    # remove the raw file
    cmd = "rm -f mp3tooggintermediatewav"
    (rawstatus, rawoutput) = commands.getstatusoutput(cmd)
    outputtologfile(logfile, rawstatus, rawoutput, "Removing intermediate file...")

    # if everything succeeds, remove the mp3 file
    if mp3status == 0 and oggstatus == 0 and rawstatus == 0:
        cmd = 'rm -f "' + mp3file + '"'
        (mp3status, mp3output) = commands.getstatusoutput(cmd)
        outputtologfile(logfile, mp3status, mp3output, "Removing MP3 file..." + mp3file)

    # mark the end of one file processing
    print >> logfile, "mp3toogg.py: '''''''''''''''''''''''''''''''''''''''''''''''''''''"


def outputtologfile(logfile, status, output, logmsg = None):
    if logmsg is not None:
        print >> logfile, "mp3toogg.py: " + logmsg
    print >> logfile, "mp3toogg.py: status " + str(status)
    print >> logfile, "mp3toogg.py: output " + output
    print >> logfile, "mp3toogg.py: ---------"


# print the license
print '''
mp3toogg.py
an MP3 to OGG converter
Copyright (C) 2007 C. Jayakumar
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.  See the GNU General Public License
for more details at <http://www.gnu.org/licenses/>.

Converting MP3 files to OGG files.  This might take some time.
'''

# find the current directory
currdir = os.getcwd()

# open the logfile
logfile = file("mp3toogg.log", 'w')

# call the above module interface to do the needful
convertallmp3stoogg(currdir, logfile)

# close the logfile
logfile.close()
