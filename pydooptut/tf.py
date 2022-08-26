#!/usr/bin/env python
"""
@author Jaganadh Gopinadhan <jaganadhg@gmail.com>
@licence Apache 
Sample Term frequency count program
"""

from pydoop.pipes import Mapper, Reducer, Factory, runTask , InputSplit
from nltk.corpus import stopwords
import re

class TFMapper(Mapper):
	"""
	TF Mapper class
	"""

	def map(self,context):
		filename = InputSplit(context.getInputSplit()).filename.split("/")[-1]
		stops = stopwords.words('english')
		words = re.compile(r'[^A-Z^a-z]+').split(context.getInputValue().\
		lower())
		for word in words:
			if word not in stops:
				context.emit(word + "@" + filename,'1')


class TFReducer(Reducer):
	"""
	TF Reducer class
	"""

	def reduce(self,context):
		count = 0
		while context.nextValue():
			count += int(context.getInputValue())

		context.emit(context.getInputKey(), str(count))

runTask(Factory(TFMapper,TFReducer))

