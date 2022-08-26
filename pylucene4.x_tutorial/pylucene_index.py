#!/usr/bin/env python
"""
PyLucene 4.x Indexing Example
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
Author Jaganadh Gopinadhan
Email jaganadhg@gmail.com
"""
import os,sys,time

import lucene

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version



class Indexer(object):
	"""
	Indexing .txt files using PyLucene
	"""

	def __init__(self,txt_file_dir,index_dir):
		"""
		:params str: txt_file_dir
		:params str: index_dir
		"""
		if not os.path.exists(index_dir):
			os.mkdir(index_dir)

		fsdir = SimpleFSDirectory(File(index_dir))
		analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
		index_config = IndexWriterConfig(Version.LUCENE_CURRENT,analyzer)
		index_config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
		index_writer = IndexWriter(fsdir,index_config)

		self.index_documents(txt_file_dir,index_writer)
		index_writer.commit()
		index_writer.close()

	def index_documents(self,txt_file_dir,index_writer):
		"""
		Performs the indexing job
		:param str: txt_file_dir
		:param writer: index_writer
		"""
		docname = FieldType()
		docname.setIndexed(True)
		docname.setStored(True)
		docname.setTokenized(False)
		docname.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)
		
		contents = FieldType()
		contents.setIndexed(True)
		contents.setStored(True)
		contents.setTokenized(True)
		contents.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

		for txt_file_dir,dir_names,file_names in os.walk(txt_file_dir):
			for filename in file_names:
				if self.is_txt(filename):
					try:
						file_path = os.path.join(txt_file_dir,filename)
						print file_path
						file_ = open(file_path)
						file_contents = file_.read()
						file_.close()
						document = Document()
						document.add(Field("file_name",file_path,docname))
					
						if len(file_contents) > 0:
							document.add(Field("contents",file_contents,contents))

						index_writer.addDocument(document)

					except Exception, exception:
						print "Failed to create Index", exception



	def is_txt(self,file_name):
		"""
		Checks if filename ends with .txt
		:params filename: str
		:returns True: bool
		"""
		if file_name.endswith(".txt"):
			return True
		else:
			return False

if __name__ == "__main__":
	lucene.initVM()
	txt_dir = sys.argv[1]
	index_dir = sys.argv[2]
	Indexer(txt_dir,index_dir)
	print "Done"
