from datetime import datetime, timedelta

from google.appengine.ext import ndb


APP_KEY_TEMPLATE = '{}-{}'
FUNC_KEY_TEMPLATE = '{}-{}-{}'

class ApplicationReportEntry(ndb.Model):
    name = ndb.StringProperty()
    count = ndb.IntegerProperty(default=0)
    date = ndb.DateProperty()
    @classmethod
    def build_id(cls,name, date):
        return APP_KEY_TEMPLATE.format(name,date)


class FunctionReportEntry(ndb.Model):
    name = ndb.StringProperty()
    count = ndb.IntegerProperty(default=0)
    date = ndb.DateTimeProperty()
    total =ndb.IntegerProperty(default=0)
    @classmethod
    def build_id(cls,name, date,hour):
        return FUNC_KEY_TEMPLATE.format(name,date,hour)

    @classmethod
    def get_one(cls, name,date,hour):
        key = cls.build_id(name,date,hour)
        return cls.get_or_insert(key)

    @classmethod
    def getEntriesLastHours(cls, hours, page, pagesize):
        now = datetime.today()
        now = now.replace(minute=00, second = 00)
        past = now - timedelta(hours=REPORT_HOURS)
        cls.query().filter(cls.date == past)


    def setAccumulated(self, q):
        self.total = self.count + q
    def setCount(self, q):
        accumulated=self.total - self.count
        self.count = q
        self.setAccumulated(accumulated)