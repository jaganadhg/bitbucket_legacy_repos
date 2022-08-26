#!/usr/bin/env python
"""
Inverted Index with pydoop
"""
from pydoop.pipes import Mapper, Reducer, Factory, runTask, InputSplit

class InvertedIndexMapper(Mapper):
	"""
	Map class
	"""

	def map(self,context):
		filename = InputSplit(context.getInputSplit()).filename.split("/")[-1]
		words = context.getInputValue().split()
		for word in words:
			context.emit(word,filename)

class InvertedIndexReducer(Reducer):
	"""
	Reduce class
	"""
	def reduce(self,context):
		first = True
		vals = ""
		while context.nextValue():
			if not first:
				vals = vals + "," + context.getInputValue()
			first = False
			vals = vals + context.getInputValue()
		context.emit(context.getInputKey(),vals)


runTask(Factory(InvertedIndexMapper,InvertedIndexReducer))
