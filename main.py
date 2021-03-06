import webapp2
from datetime import datetime
import json
import logging

from google.appengine.api import taskqueue
from google.appengine.datastore.datastore_query import Cursor

import shardCounter.report as report
import resthandler

FUNCTIONS_PAGE_SIZE = 10
APPLICATIONS_PAGE_SIZE = 10


class ApplicationsHandler(resthandler.RestHandler):
    def get(self):
        nextc = self.request.get("next")
        date = datetime.today()
        if nextc:
            (q, cursor, more) = report.ApplicationReportEntry.getEntriesByDate(
                date).fetch_page(page_size=APPLICATIONS_PAGE_SIZE,
                                 start_cursor=Cursor.from_websafe_string(nextc))
        else:
            (q, cursor, more) = report.ApplicationReportEntry.getEntriesByDate(
                date).fetch_page(page_size=APPLICATIONS_PAGE_SIZE)
        q = [{'name': e.name, 'count': e.count, 'date': e.date.isoformat()} for
             e in q]
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
            (q, cursor, more) = report.FunctionReportEntry.getEntriesLastHours(
                time).fetch_page(page_size=FUNCTIONS_PAGE_SIZE,
                                 start_cursor=Cursor.from_websafe_string(nextc))
        else:
            (q, cursor, more) = report.FunctionReportEntry.getEntriesLastHours(
                time).fetch_page(page_size=FUNCTIONS_PAGE_SIZE)
        q = [{'name': e.name, 'total': e.total, 'date': e.date.isoformat()} for
             e in q]
        response = {}
        response['result'] = q
        response['more'] = more
        if more:
            response['next'] = cursor.to_websafe_string()
        self.SendJson(response)


class ReportHandler(resthandler.RestHandler):
    def post(self):
        logging.debug(self.request)
        body = self.readJson()

        queue = taskqueue.Queue(name='analysis')
        logging.debug(json.dumps(body))
        task = taskqueue.Task(url='/',
                              target='analyzer',
                              payload=json.dumps(body),
                              method="PUT")

        queue.add(task)
        self.SendJsonOKMessage('Analyze queued')


APP = webapp2.WSGIApplication([
    ('/rest/applications', ApplicationsHandler),
    ('/rest/functions', FunctionsHandler),
    ('/rest/report', ReportHandler),
], debug=True)
