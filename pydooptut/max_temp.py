#!/usr/bin/env python
"""
Pydoop version of maximum temperature program in Hadoop the Definitave
Guide by Tom White
@author Jaganadh Gopinadhan
@copyright Apache Licence
"""
import sys
from pydoop.pipes import Mapper, Reducer, Factory, runTask

class MaxTempMapper(Mapper):
	"""
	Max Temperature mapper class
	"""

	def __init__(self,context):
		super(MaxTempMapper, self).__init__(context)
		self.MISSING = 9999
		self.qmap = "01459"
	
	def map(self,context):
		line = context.getInputValue().strip()
		year = int(line[15:19])
		air_temp = 0

		if line[87] == '+':
			air_temp = int(line[88:92])
		else:
			air_temp = int(line[87:92])
		quality = line[92:93]

		if air_temp != self.MISSING and quality in self.qmap:
			context.emit(str(year), str(air_temp))


class MaxTempReucer(Reducer):
	"""
	Max temperature reducer
	"""

	def __init__(self,context):
		super(MaxTempReucer, self).__init__(context)
	
	def reduce(self,context):
		max_value = -sys.maxint - 1
		while context.nextValue():
			max_value = max(max_value, int(context.getInputValue()))

		context.emit(context.getInputKey(), str(max_value))

runTask(Factory(MaxTempMapper,MaxTempReucer))
