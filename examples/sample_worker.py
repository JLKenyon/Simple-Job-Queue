#!/usr/bin/python

import xmlrpclib
import time

print "Starting up"
server = xmlrpclib.Server("http://localhost:16180")
print "Server found"
myId = server.nextWorkerId()
print "My Worker ID is ",myId

while True:
    print "Waiting for a job"
    jid,job = server.getJob(myId)
    print "Got a job: ",job
    val = job*job
    time.sleep(5)
    server.postResult(myId,jid,val)
    print "Posted result"
