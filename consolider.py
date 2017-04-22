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
import json

from google.appengine.api import taskqueue
from google.appengine.datastore.datastore_query import Cursor

import shardCounter.namedShardCounters as counters
import resthandler

CHUNK_SIZE_FUNC=15
CHUNK_SIZE_APP=50
DATE_FORMAT='%Y-%m-%dT%H:%M:%S.%f'
class FunctionHandler(resthandler.RestHandler):
	def put(self):
		

		body = self.readJson()

		if body.get("cursor"):
			logging.info("Continuing consolidation of functions")
			(q, cursor, more)= counters.FunctionCounter.get_dirties().fetch_page(page_size=CHUNK_SIZE_FUNC, 
				start_cursor=Cursor.from_websafe_string(body.get("cursor")))
		else:
			logging.info("Starting consolidation of functions")
			(q, cursor, more)= counters.FunctionCounter.get_dirties().fetch_page(page_size=CHUNK_SIZE_FUNC)
			
		logging.info("{} Function Records taken".format(len(q)))
		for f in q:
			counters.FunctionCounter.consolidate(f)
		if more:
			task = taskqueue.add(url='/function',target='consolider',method='PUT',payload="{\"cursor\": \"%s\"}" % cursor.to_websafe_string())
			logging.info("Queueing taks in order to continue consolidating functions")
			self.SendJsonOKMessage('Task {} enqueued, ETA {}.'.format(task.name, task.eta))
		else:
			logging.info("Consolidation of functions done")
			self.SendJsonOKMessage('Consolidation done')
			

class ApplicationHandler(resthandler.RestHandler):
	def put(self):
		

		body = self.readJson()

		if body.get("cursor"):
			logging.info("Continuing consolidation of applications")
			(q, cursor, more)= counters.ApplicationCounter.get_dirties().fetch_page(page_size=CHUNK_SIZE_APP, 
				start_cursor=Cursor.from_websafe_string(body.get("cursor")))
		else:
			logging.info("Starting consolidation of applications")
			(q, cursor, more)= counters.ApplicationCounter.get_dirties().fetch_page(page_size=CHUNK_SIZE_APP)
			
		logging.info("{} Application Records taken".format(len(q)))
		for f in q:
			counters.ApplicationCounter.consolidate(f)
		if more:
			task = taskqueue.add(url='/application',target='consolider',method='PUT',payload="{\"cursor\": \"%s\"}" % cursor.to_websafe_string())
			logging.info("Queueing taks in order to continue consolidating applications")
			self.SendJsonOKMessage('Task {} enqueued, ETA {}.'.format(task.name, task.eta))
		else:
			logging.info("Consolidation of applications done")
			self.SendJsonOKMessage('Consolidation done')
		

app = webapp2.WSGIApplication([
	('/function', FunctionHandler),
	('/application', ApplicationHandler),
], debug=True)
