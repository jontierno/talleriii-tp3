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
import shardCounter.namedShardCounters as counters
from datetime import datetime,timedelta
import logging
import resthandler 

class ApplicationCounterHandler(resthandler.RestHandler):
    def put(self):
        body = self.readJson()
        timestamp = dt_parse(body.get("timestamp"))
        logging.debug("Registering error to application %s on %s",body.get("application"),body.get("timestamp"))
        counters.ApplicationCounter.increment(body.get("application"), timestamp)


class FunctionCounterHandler(resthandler.RestHandler):
    def put(self):
        body = self.readJson()
        timestamp = dt_parse(body.get("timestamp"))
        logging.debug("Registering error to function %s on %s",body.get("function"),body.get("timestamp"))
        counters.FunctionCounter.increment(body.get("function"), timestamp)



def dt_parse(t):
    ret = datetime.strptime(t[0:16],'%Y-%m-%dT%H:%M')
    if t[18]=='+':
        ret+=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
    elif t[18]=='-':
        ret-=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
    return ret

app = webapp2.WSGIApplication([
    ('/application', ApplicationCounterHandler),
    ('/function', FunctionCounterHandler),
], debug=True)
