
import webapp2
import logging
import json

from google.appengine.api import taskqueue
from google.appengine.datastore.datastore_query import Cursor

import shardCounter.namedShardCounters as counters
import resthandler

CHUNK_SIZE_FUNC = 15
CHUNK_SIZE_APP = 50
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


class FunctionHandler(resthandler.RestHandler):
    def put(self):

        body = self.readJson()

        if body.get("cursor"):
            logging.info("Continuing consolidation of functions")
            (q, cursor,
             more) = counters.FunctionCounter.get_dirties().fetch_page(
                page_size=CHUNK_SIZE_FUNC,
                start_cursor=Cursor.from_websafe_string(
                    body.get("cursor")))
        else:
            logging.info("Starting consolidation of functions")
            (q, cursor,
             more) = counters.FunctionCounter.get_dirties().fetch_page(
                page_size=CHUNK_SIZE_FUNC)

        logging.info("{} Function Records taken".format(len(q)))
        if more:
            task = taskqueue.add(url='/function', target='consolidator',
                                 method='PUT',
                                 payload="{\"cursor\": \"%s\"}" % cursor.to_websafe_string())
            logging.info(
                "Queueing taks in order to continue consolidating functions")

        for f in q:
            counters.FunctionCounter.consolidate(f)
        logging.info("{} Function Records proccessed".format(len(q)))
        if more:
            self.SendJsonOKMessage(
                'Task {} enqueued, ETA {}.'.format(task.name, task.eta))
        else:
            logging.info("Consolidation of functions done")
            self.SendJsonOKMessage('Consolidation done')

    def get(self):
        self.put()


class ApplicationHandler(resthandler.RestHandler):
    def put(self):

        body = self.readJson()

        if body.get("cursor"):
            logging.info("Continuing consolidation of applications")
            (q, cursor,
             more) = counters.ApplicationCounter.get_dirties().fetch_page(
                page_size=CHUNK_SIZE_APP,
                start_cursor=Cursor.from_websafe_string(
                    body.get("cursor")))
        else:
            logging.info("Starting consolidation of applications")
            (q, cursor,
             more) = counters.ApplicationCounter.get_dirties().fetch_page(
                page_size=CHUNK_SIZE_APP)

        logging.info("{} Application Records taken".format(len(q)))
        if more:
            task = taskqueue.add(url='/application', target='consolidator',
                                 method='PUT',
                                 payload="{\"cursor\": \"%s\"}" % cursor.to_websafe_string())
            logging.info(
                "Queueing taks in order to continue consolidating applications")

        for f in q:
            counters.ApplicationCounter.consolidate(f)
        logging.info("{} Application Records proccessed".format(len(q)))
        if more:
            self.SendJsonOKMessage(
                'Task {} enqueued, ETA {}.'.format(task.name, task.eta))
        else:
            logging.info("Consolidation of applications done")
            self.SendJsonOKMessage('Consolidation done')

    def get(self):
        self.put()


app = webapp2.WSGIApplication([
    ('/function', FunctionHandler),
    ('/application', ApplicationHandler),
], debug=True)
