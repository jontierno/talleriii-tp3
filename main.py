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

import json

import webapp2

import model


def AsDict(guest):
    return {'id': guest.key.id(), 'first': guest.first, 'last': guest.last}


class RestHandler(webapp2.RequestHandler):

    def dispatch(self):
        # time.sleep(1)
        super(RestHandler, self).dispatch()

    def SendJson(self, r):
        self.response.headers['content-type'] = 'application/json'
        self.response.write(json.dumps(r))


class ApplicationsHandler(RestHandler):

    def get(self):
        r = []
        v = {}
        r.append({'name':"app1", 'count':10})
        self.SendJson(r)


class FunctionsHandler(RestHandler):
    def get(self):
        r = []
        v = {}
        r.append({'name':"funct", 'count':10})
        self.SendJson(r)

APP = webapp2.WSGIApplication([
    ('/rest/applications', ApplicationsHandler),
    ('/rest/functions', FunctionsHandler),
], debug=True)
