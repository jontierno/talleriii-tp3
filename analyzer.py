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
import re
from google.appengine.api import taskqueue
import resthandler

class AnalyzerHandler(resthandler.RestHandler):
	def put(self):
		logging.debug(self.request.body)
		body = self.readJson()
		trace = body.get("trace")
		application = body.get("application")
		timestamp = body.get("timestamp")

		queue = taskqueue.Queue(name='count')
		task = taskqueue.Task(url='/application',
			target='counter',
			payload="{\"application\": \"%s\", \"timestamp\": \"%s\"}" % (application,timestamp),
			method="PUT")

		rpc = queue.add_async(task)
		rpcs = []
		for f in re.findall('at (.+)\(', trace):		
			task = taskqueue.Task(
				url='/function',
				target='counter',
				payload="{\"function\": \"%s\", \"timestamp\": \"%s\"}" % (f,timestamp),
				method="PUT")
			logging.debug(f)
			rpcs.append(queue.add_async(task))
		rpc.get_result()
		for rpc in rpcs:
			rpc.get_result()
		self.SendJsonOKMessage('Analyze done, update tasks queued')

app = webapp2.WSGIApplication([
	('/', AnalyzerHandler),
], debug=True)

