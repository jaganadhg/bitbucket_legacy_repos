#!/usr/bin/env python
"""
Author : Jaganadh Gopinadhan
e-mail : jaganadhg@gmail.com
Licence : Apache 
"""
import sys
from pydoop.pipes import Mapper, Reducer, Partitioner,Factory, runTask

class WordCountMapper(Mapper):
	"""
	Mapper class
	"""
	def __init__(self,context):
		super(WordCountMapper,self).__init__(self)

	def map(self,context):
		words = context.getInputValue().split()
		for word in words:
			context.emit(word,"1")

class WordCountReducer(Reducer):
	"""
	Reducer class
	"""
	def __init__(self,context):
		super(WordCountReducer,self).__init__(self)

	def reduce(self,context):
		count = 0
		while context.nextValue():
			count += int(context.getInputValue())

		context.emit(context.getInputKey(), str(count))


class WordCountPartitioner(Partitioner):
	"""
	Partitioner class
	"""
	def __init__(self,context):
		super(WordCountPartitioner,self).__init__(self)

	def partition(self,key,num_of_reducers):
		reducer_id = (hash(key) & sys.maxint) & num_of_reducers
		return reducer_id


runTask(Factory(WordCountMapper, WordCountReducer,\
partitioner_class=WordCountPartitioner,combiner_class=WordCountReducer))
