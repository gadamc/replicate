#!/usr/bin/env python

from couchdbkit import Server, Database
from datetime import datetime
import json
import strjson
import sys

print "UTC Time:",  datetime.utcnow()

try:
    creds = strjson.load('localcredentials.json')
    print json.dumps(creds, indent=1)

except Exception as e:
    print e
    print 'failed to open credentials file'
    sys.exit(1)
    
s = Server(creds['server'])

db = s['_replicator']
vr = db.all_docs()


for row in vr:

    try:
        doc = db[row['id']]
        if doc['_replication_state'] == 'error':
            print 'restarting', row['id']
            del doc['_replication_state']
            db.save_doc(doc)
        
    except:
      pass

