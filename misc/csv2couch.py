#!/usr/bin/python
import csv
import sys
import couchdb
#author - Jaganadh G jaganadhg@gmail.com
#licence - given to every body . Modify it and use it as you wish

def csv2Couch(csvfile,dbname,delim=',',qcr='"'):
	csvcont = csv.DictReader(open(csvfile, 'r'), delimiter = delim, quotechar = qcr)
	datas = [cont for cont in csvcont]
	server = couchdb.Server()
	#assumes that couchdb runs on http://localhost:5984
	db = server[dbname]
	#assumes that db is already created

	for data in datas:
		document = data
		print document
		db[str(datas.index(data))] = document
		#to assign a unique id for each document

if __name__ == '__main__':
	fname = sys.argv[1]
	dbname = sys.argv[2]
	csv2Couch(fname,dbname)
