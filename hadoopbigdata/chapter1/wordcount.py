#!/usr/bin/env python
"""
Author : Jaganadh Gopinadhan
e-mail : jaganadhg@gmail.com
Licence : Apache 
"""

from pydoop.pipes import Mapper, Reducer, Factory, runTask

class WordCountMapper(Mapper):
	"""
	Mapper class
	"""
	def map(self,context):
		words = context.getInputValue().split()
		for word in words:
			context.emit(word,"1")

class WordCountReducer(Reducer):
	"""
	Reducer class
	"""
	def reduce(self,context):
		count = 0
		while context.nextValue():
			count += int(context.getInputValue())

		context.emit(context.getInputKey(), str(count))


runTask(Factory(WordCountMapper, WordCountReducer))
