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


CHUNK_SIZE_FUNC=10
CHUNK_SIZE_APP=10

class FunctionHandler(webapp2.RequestHandler):
    def put(self):
        logging.info("Starting consolidation of functions")
        q = counters.FunctionCounter.get_dirties().fetch(limit=CHUNK_SIZE_FUNC)
        for f in q:
			counters.FunctionCounter.consolidate(f)  

class ApplicationHandler(webapp2.RequestHandler):
    def put(self):
    	logging.info("Starting consolidation of applications")
        q = counters.ApplicationCounter.get_dirties().fetch(limit=CHUNK_SIZE_APP)
        for element in q:
			counters.ApplicationCounter.consolidate(element)        


app = webapp2.WSGIApplication([
    ('/function', FunctionHandler),
    ('/application', ApplicationHandler),
], debug=True)
