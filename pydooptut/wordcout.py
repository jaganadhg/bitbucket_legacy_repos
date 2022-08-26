#!/usr/bin/env python

from pydoop.pipes import Mapper, Reducer, Factory, runTask

class WordCountMapper(Mapper):
	"""
	Map class
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


#if __name__ == "__main__":
runTask(Factory(WordCountMapper, WordCountReducer))
