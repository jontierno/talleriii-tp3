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
                              payload="{\"application\": \"%s\", \"timestamp\": \"%s\"}" % (
                              application, timestamp),
                              method="PUT")

        rpc = queue.add_async(task)
        rpcs = []
        lines = trace.split(" at ")
        lines.pop(0)
        pattern = re.compile('at (.+)\(')
        for f in lines:
            # f = match.group(0)
            task = taskqueue.Task(
                url='/function',
                target='counter',
                payload="{\"function\": \"%s\", \"timestamp\": \"%s\"}" % (
                f, timestamp),
                method="PUT")
            rpcs.append(queue.add_async(task))
            rpc.get_result()
        for rpc in rpcs:
            rpc.get_result()

        self.SendJsonOKMessage('Analyze done, update tasks queued')


app = webapp2.WSGIApplication([
    ('/', AnalyzerHandler),
], debug=True)
