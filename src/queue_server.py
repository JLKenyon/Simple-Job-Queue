#!/usr/bin/python
# Copyright (c) 2010 John Kenyon
#  
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#  
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#  
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import SocketServer
import SimpleXMLRPCServer
import threading
from Queue import Queue
from Queue import Empty

def idMaker():
    id = 1
    while True:
        yield id
        id += 1

class JobQueue:
    nextWorkerId = idMaker().next
    nextJobId = idMaker().next
    inQueue = Queue()
    outQueue = Queue()
    pending = {}
    def postJob(self,job):
        print "postJob"
        jid = self.nextJobId()
        self.inQueue.put( (jid,job) )
        print "Recieved job:",job
        return jid
    def getJob(self,myId):
        print "getJob"
        jid,job = self.inQueue.get()
        self.pending[jid] = job
        print "Delegated job:",job
        return jid,job
    def postResult(self,myId,jid,value):
        print "postResult"
        if self.pending.has_key(jid):
            del self.pending[jid]
            self.outQueue.put( (jid,value) )
            print "Job was finished"
        else:
            print "Serious error has occured"
        return True
    def getResult(self):
        print "getResult"
        val = self.outQueue.get()
        print "Result was sent"
        return val

class AsyncXMLRPCServer(SocketServer.ThreadingMixIn,
                        SimpleXMLRPCServer.SimpleXMLRPCServer): pass

if __name__=="__main__":
    server = AsyncXMLRPCServer(("localhost",16180))
    server.register_instance(JobQueue())
    server.serve_forever()


