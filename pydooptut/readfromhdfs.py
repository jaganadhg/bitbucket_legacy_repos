#!/usr/bin/env python
"""
Read a file from hadoop and print the contents
The program assumes that the file is located in
the root dir of HDFS
"""
from pydoop import hdfs

def readfile(filename):
	infile = hdfs.open(filename,'r')
	content = infile.read()
	print content


if __name__ == "__main__":
	fname = "samp_py.txt"
	readfile(fname)
