#!/usr/bin/python
#-*-coding:utf-8

from kmeans import *
import os
import sys
import pdb

def main():
    if len(sys.argv) != 5:
        print >> sys.stderr,"Usage [%s] [word_dict] [center_file] [input_file] [output_file]" % (sys.argv[0])
        sys.exit(1)
    word_dict = sys.argv[1]
    center_file = sys.argv[2]
    input_file = sys.argv[3]
    output_file = sys.argv[4]

    #pdb.set_trace()
    km = KMeans(word_dict,5)
    km.init_center(center_file)
    km.cluster(input_file,output_file)
if __name__ == "__main__":
    main()
