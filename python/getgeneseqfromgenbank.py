#!/usr/bin/env python

# getgeneseqfromgenbank.py
# gets the name and sequence of gene(s) from a Genbank file
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

# This script takes a Genbank file as input, and reads the feature list
#      for any gene features.  It collects information about the gene and
#      the sequence of the gene and prints them out to the given outputfile.
#      it prints to the output file in the following comma-delimited format
#      /gene,/note,/locus_tag,sequence
# It uses the Biopython module (www.biopython.org).
# The GenBank sequence file should be in the same directory as the script.
# What you need to have:
#      1.  Python 2.5.1
#      2.  BioPython 1.43.2
# How to run the script:
#     run 'python <script filename>  <inputfile e.g sequence file> <outputfile>'
# Caveats
#     if the <outputfile> already exists, it is OVERWRITTEN.
# What it does
#     it searches the 'features' in a GenBank file for the 'gene' feature.
#     Once a 'gene' feature is found, it looks for the required information
#     It also looks for the gene location and gets the actual gene from the whole
#     gene sequence present in the GenBank file, after performing any complement
#     (with reversing) operation on the sequence

# print the license
print '''
getgeneseqfromgenbank.py
gets the name and sequence of gene(s) from a Genbank file
Copyright (C) 2007 C. Jayakumar
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.  See the GNU General Public License
for more details at <http://www.gnu.org/licenses/>.
'''

import sys
from os.path import exists

# verify that the proper number of arguments are passed-in
if len(sys.argv) != 3:
    print "Usage: getgeneseqfromgenbank.py <inputfile> <outputfile>"
    quit()

# verify that the input file is valid
inputfile = sys.argv[1]
if not exists(inputfile):
    print "Error: %s does not exist or cannot be read." % inputfile
    quit()

outputfile = sys.argv[2]
outputfilehandle = open(sys.argv[2], "w")

# print the start
print "Getting the gene information and appending to the outputfile..."

# get the sequence
from Bio import SeqIO
for seq_record in SeqIO.parse(open(inputfile, "r"), "genbank") :
    genomeseq = seq_record.seq

# get the feature list
from Bio import GenBank
feature_parser = GenBank.FeatureParser()
gb_record = feature_parser.parse(open(inputfile, "r"))

# get and print to the output file, the required information of each gene
for featur in gb_record.features:
    if featur.type == 'gene':
        if featur.strand == 1:
            geneseq = (genomeseq[featur.location.nofuzzy_start:featur.location.nofuzzy_end]).tostring()
            start = featur.location.nofuzzy_start
            end = featur.location.nofuzzy_end
            sense = "sense"
        elif featur.strand == -1:
            geneseq = ((genomeseq[featur.location.nofuzzy_start:featur.location.nofuzzy_end]).reverse_complement()).tostring()
            start = featur.location.nofuzzy_end
            end = featur.location.nofuzzy_start
            sense = "anti-sense"

        if featur.qualifiers.has_key('gene'):
            genename = featur.qualifiers['gene']
        else:
            genename = ''

        if featur.qualifiers.has_key('note'):
            genenote = featur.qualifiers['note']
        else:
            genenote = ''

        if featur.qualifiers.has_key('locus_tag'):
            genelocustag = featur.qualifiers['locus_tag']
        else:
            genelocustag = ''


        # print to the output file in the following comma-delimited format
        # /gene,/note,/locus_tag,sequence
        # should probably use the CSV module here
        print >> outputfilehandle, '%s~%s~%s~%i~%i~%s~%s' % (genename, genenote, genelocustag, start, end, sense, geneseq)

# close all open resources
outputfilehandle.close()

# print the completion
print 'Done.'
