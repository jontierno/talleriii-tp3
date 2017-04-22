# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import logging
import shardCounter.namedShardCounters as counters
from google.appengine.api import taskqueue
from datetime import datetime,timedelta
import json

CHUNK_SIZE_FUNC=30
CHUNK_SIZE_APP=1
DATE_FORMAT='%Y-%m-%dT%H:%M:%S.%f'
class FunctionHandler(webapp2.RequestHandler):
	def put(self):
		logging.info("Starting consolidation of functions")

		date = None
		body_unicode = self.request.body.decode('utf-8')
		logging.info(body_unicode)
		if len(body_unicode) >0:
			body = json.loads(body_unicode)	
			date = datetime.strptime(body.get("lastDate"), DATE_FORMAT) if body.get("lastDate") else datetime.min
		else:
			date = datetime.min
		

		q = counters.FunctionCounter.get_dirties(date).fetch(limit=CHUNK_SIZE_FUNC)	
		logging.info("{} Function Records taken".format(len(q)))
		for f in q:
			counters.FunctionCounter.consolidate(f)
		##f is sorter by dirty date.
		if len(q) == CHUNK_SIZE_FUNC:
			task = taskqueue.add(url='/function',target='consolider',method='PUT',payload="{\"lastDate\": \"%s\"}" % q[-1].lastDirty.strftime(DATE_FORMAT))
			logging.info("Queueing taks in order to continue consolidation of functions")
			self.response.write('Task {} enqueued, ETA {}.'.format(task.name, task.eta))
		else:
			self.response.write('Consolidation done')

class ApplicationHandler(webapp2.RequestHandler):
	def put(self):
		logging.info("Starting consolidation of applications")

		date = None
		body_unicode = self.request.body.decode('utf-8')
		logging.info(body_unicode)
		if len(body_unicode) >0:
			body = json.loads(body_unicode)	
			date = datetime.strptime(body.get("lastDate"), DATE_FORMAT) if body.get("lastDate") else datetime.min
		else:
			date = datetime.min
		

		q = counters.ApplicationCounter.get_dirties(date).fetch(limit=CHUNK_SIZE_APP)
		for element in q:
			counters.ApplicationCounter.consolidate(element)
		logging.info("{} Application Records taken".format(len(q)))
		for f in q:
			counters.ApplicationCounter.consolidate(f)
		##f is sorter by dirty date.
		if len(q) == CHUNK_SIZE_APP:
			task = taskqueue.add(url='/application',target='consolider',method='PUT',payload="{\"lastDate\": \"%s\"}" % q[-1].lastDirty.strftime(DATE_FORMAT))
			logging.info("Queueing taks in order to continue consolidation of applications")
			self.response.write('Task {} enqueued, ETA {}.'.format(task.name, task.eta))
		else:
			self.response.write('Consolidation done')

def dt_parse(t):
    ret = datetime.strptime(t,' ')
    if t[18]=='+':
        ret+=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
    elif t[18]=='-':
        ret-=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
    return ret

app = webapp2.WSGIApplication([
	('/function', FunctionHandler),
	('/application', ApplicationHandler),
], debug=True)
