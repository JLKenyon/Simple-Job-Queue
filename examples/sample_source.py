#!/usr/bin/python

import xmlrpclib
import time

server = xmlrpclib.Server("http://localhost:16180")

joblist = range(20)

jobmap = {}
jobvals = {}

for job in joblist:
    print "Posting job: %i"%(job)
    jid = server.postJob(job)
    jobmap[jid] = job

for count in range(len(joblist)):
    jid,val = server.getResult()
    print "Recieved job:",jid,val
    jobvals[jid] = val

for key in jobvals.keys():
    print "Job %i => %i"%(jobmap[key],jobvals[key])
