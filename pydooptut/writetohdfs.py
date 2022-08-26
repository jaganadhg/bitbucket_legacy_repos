#!/usr/bin/env python
"""
Open a file in hdfs and write given content to it
The program writes a file in HDFS root (/) directory
"""
from pydoop import hdfs


def writefile(filename,content):
	outfile = hdfs.open(filename,'w')
	outfile.write(content)
	outfile.close()
	print "Wrote file %s " %(filename)


if __name__ == "__main__":
	fin = "samp_py.txt"
	cont = "This is sample from pydoop"
	writefile(fin,cont)
