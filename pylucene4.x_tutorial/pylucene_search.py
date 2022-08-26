#!/usr/bin/env python
"""
PyLucene 4.x Index Searchig example
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
import os,sys
import lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version

class Searcher(object):
	"""
	Search using PyLucene
	"""

	def __init__(self,index_dir):
		"""
		:params str: index_dir
		"""
		index = SimpleFSDirectory(File(index_dir))
		analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
		self.query_parser = QueryParser(Version.LUCENE_CURRENT,"contents",analyzer)
		self.searcher_ = IndexSearcher(DirectoryReader.open(index))

	def search(self,query):
		"""
		Performs search
		:params str: query
		"""
		parsed_query = self.query_parser.parse(query)

		scored_docs = self.searcher_.search(parsed_query,10).scoreDocs

		for doc in scored_docs:
				doc_ = self.searcher_.doc(doc.doc)
				print doc_.get("file_name"), doc_.get("contents")

if __name__ == "__main__":
	lucene.initVM()
	index = sys.argv[1]
	searcher = Searcher(index)
	query = "watch"
	searcher.search(query)
	
