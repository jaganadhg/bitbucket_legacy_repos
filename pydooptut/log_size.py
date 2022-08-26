#!/usr/bin/env python
import sys
import re
from pydoop.pipes import Mapper,Reducer,Factory,runTask

class HitMapper(Mapper):

        def __init__(self,context):
                super(HitMapper, self).__init__(context)
                self.pattern = re.compile("([^\\s]+) - - \\[(.+)\\] \"([^\\s]+) (/[^\\s]*) HTTP/[^\\s]+\" [^\\s]+ ([0-9]+)")

        def map(self,context):
                log = context.getInputValue()
                match_ = self.pattern.match(log)
                if match_ != None:
                	size = match_.group(5)
                	context.emit("MessageSize",size)

class HitReducer(Reducer):
        def __init__(self,context):
                super(HitReducer, self).__init__(context)
                self.total = 0
                self.count = 0
                self.min_ = sys.maxint
                self.max_ = 0

        def reduce(self,context):
                while context.nextValue():
                        size = int(context.getInputValue())
                        self.total = size + self.total
                        self.count += 1
                        if size < self.min_:
                                self.min_ = size
                        if size > self.max_:
                                self.max_ = size
                context.emit("Mean", str(self.total / self.count))
                context.emit("Max",str(self.max_))
                context.emit("Min",str(self.min_))


if __name__ == "__main__":
        runTask(Factory(HitMapper,HitReducer))


