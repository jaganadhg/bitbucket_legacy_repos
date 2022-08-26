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
                	url = match_.group(4)
                	context.emit(url,"1")

class HitReducer(Reducer):
        def __init__(self,context):
                super(HitReducer, self).__init__(context)

        def reduce(self,context):
                count = 0
                while context.nextValue():
                        count += int(context.getInputValue())
                context.emit(context.getInputKey(),str(count))


if __name__ == "__main__":
        runTask(Factory(HitMapper,HitReducer))


