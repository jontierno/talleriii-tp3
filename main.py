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
from datetime import datetime

from google.appengine.api import taskqueue
from google.appengine.datastore.datastore_query import Cursor

import shardCounter.report as report
import resthandler

FUNCTIONS_PAGE_SIZE=10
APPLICATIONS_PAGE_SIZE=10
class ApplicationsHandler(resthandler.RestHandler):
    def get(self):
        nextc = self.request.get("next")
        date = datetime.strptime(self.request.get("date")[0:10],'%Y-%m-%d')
        if nextc:
            (q, cursor, more)= report.ApplicationReportEntry.getEntriesByDate(date).fetch_page(page_size=APPLICATIONS_PAGE_SIZE, 
                start_cursor=Cursor.from_websafe_string(nextc))
        else:
            (q, cursor, more)= report.ApplicationReportEntry.getEntriesByDate(date).fetch_page(page_size=APPLICATIONS_PAGE_SIZE)
        q = [{'name': e.name, 'count': e.count, 'date': e.date.isoformat()} for e in q] 
        response = {}
        response['result'] = q
        response['more'] = more
        if more:
            response['next'] = cursor.to_websafe_string()
        self.SendJson(response)


class FunctionsHandler(resthandler.RestHandler):
    def get(self):
        nextc = self.request.get("next")
        time = int(self.request.get("time"))
        if nextc:
            (q, cursor, more)= report.FunctionReportEntry.getEntriesLastHours(time).fetch_page(page_size=FUNCTIONS_PAGE_SIZE, 
                start_cursor=Cursor.from_websafe_string(nextc))
        else:
            (q, cursor, more)= report.FunctionReportEntry.getEntriesLastHours(time).fetch_page(page_size=FUNCTIONS_PAGE_SIZE)
        q = [{'name': e.name, 'total': e.total, 'date': e.date.isoformat()} for e in q] 
        response = {}
        response['result'] = q
        response['more'] = more
        if more:
            response['next'] = cursor.to_websafe_string()
        self.SendJson(response)

class ReportHandler(resthandler.RestHandler):
    def post(self):
        body = self.readJson()
        r.append({'name':"app1", 'count':10})
        self.SendJson(r)


APP = webapp2.WSGIApplication([
    ('/rest/applications', ApplicationsHandler),
    ('/rest/functions', FunctionsHandler),
    ('/rest/report', FunctionsHandler),
], debug=True)
