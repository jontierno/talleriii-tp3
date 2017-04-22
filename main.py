# Copyright 2013 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#             http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import resthandler
from google.appengine.api import taskqueue

class ApplicationsHandler(resthandler.RestHandler):
    def get(self):
        body = self.readJson()


class FunctionsHandler(resthandler.RestHandler):
    def get(self):
        body = self.readJson()
        r = []
        v = {}
        r.append({'name':"funct", 'count':10})
        self.SendJson(r)

class ReportHandler(RestHandler):
    def post(self):
        body = self.readJson()
        r.append({'name':"app1", 'count':10})
        self.SendJson(r)


APP = webapp2.WSGIApplication([
    ('/rest/applications', ApplicationsHandler),
    ('/rest/functions', FunctionsHandler),
    ('/rest/report', FunctionsHandler),
], debug=True)
