#!/usr/bin/env python
"""
@author = Jaganadh Gopinadhan  <jaganadhg@gmail.com>
@licence Apache

Docuemnt Frequency counting with pydoop
"""
import struct
from pydoop.pipes import Mapper, Reducer, Factory, runTask, InputSplit,\
RecordReader, RecordWriter
from pydoop.utils import jc_configure, jc_configure_int
import pydoop.hdfs as hdfs
import logging


class DFMapper(Mapper):
	"""
	DF Mapper class
	"""

	def __init__(self,context):
		super(DFMapper, self).__init__(context)

	def map(self,context):
		wdcount = context.getInputSplit()
		word_count = wdcount.split()
		word_doc = word_count[0].split('@')
		print word_doc
		context.emit(word_doc[1], word_doc[0] + "=" + word_count[1])
		context.emit(word_doc[1], word_doc[0] + "=" + count)


class DFReducer(Reducer):
	"""
	Reducer class
	"""

	def __init__(self,context):
		super(DFReducer, self).__init__(context)

	def reduce(self,context):
		count = 0
		doc_count = {}
		while context.nextValue():
			word_doc_count = context.getInputValue().split("=")
			doc_count[word_doc_count[0]] = int(word_doc_count[1])
			count += int(word_doc_count[1])
			
			for key in doc_count.keys():
				context.emit(key, doc_count[key] + "/" + str(count))


class Reader(RecordReader):
	"""
	Record reader
	"""

	def __init__(self,context):
		"""
		"""
		super(Reader,self).__init__(context)
		job_conf = context.getJobConf()
		jc_configure_int(self,job_conf,"","")
		jc_configure(self,job_conf,"mapred.input.format.class",\
		"org.apache.hadoop.mapred.SequenceFileInputFormat")
		self.inputsplit = InputSplit(context.getInputSplit())
		self.inputfile = hdfs.open(self.inputsplit.filename)
		self.inputfile.seek(self.inputsplit.offset)
		self.bytes_read = 0

		if self.inputsplit.offset > 0:
			discarded = self.inputfile.readline()
			self.bytes_read += len(discarded)
	
	def close(self):
		self.inputfile.close()
		self.inputfile.fs.close()
	
	def next(self):
		if self.bytes_read > self.inputsplit.length:
			return (False, "", "")

		key = struct.pack(">q", self.inputsplit.offset + self.bytes_read)
		record = self.inputfile.readline()

		if record == "":
			return (False, "", "")

		self.bytes_read = len(record)
		return (True, key, record)

	def getProgress(self):
		return min(float(self.bytes_read)/self.inputsplit.length,1.0)

class Writer(RecordWriter):

	def __init__(self,context):
		super(Writer, self).__init__(context)
		job_conf = context.getJobConf()
		jc_configure_int(self,job_conf,"mapred.task.partition", "part")
		jc_configure(self,job_conf,"mapred.work.output.dir", "outdir")
		jc_configure(self,job_conf,"mapred.textoutputformat.separator", "sep", "\t")
		self.outfn = "%s/part-%05d" % (self.outdir, self.part)
		self.file = hdfs.open(self.outfn, "w")
	
	def close(self):
		self.file.close()
		self.file.fs.close()
	
	def emit(self):
		self.file.write("%s%s%s\n" % (key, self.sep, value))


runTask(Factory(DFMapper,DFReducer,record_reader_class=Reader,\
record_writer_class=Writer,combiner_class=DFReducer))
