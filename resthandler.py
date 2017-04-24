import webapp2
import json


class RestHandler(webapp2.RequestHandler):
    def dispatch(self):
        # time.sleep(1)
        super(RestHandler, self).dispatch()

    def SendJson(self, r):
        self.response.headers['content-type'] = 'application/json'
        self.response.write(json.dumps(r))

    def SendJsonOKMessage(self, r):
        self.response.headers['content-type'] = 'application/json'
        self.response.write(
            json.dumps({'message': r if r else 'OK', 'status': '200'}))

    def readJson(self):
        body_unicode = self.request.body.decode('utf-8')
        if len(body_unicode) > 0:
            return json.loads(body_unicode)
        return {}
