from datetime import datetime, timedelta

from google.appengine.ext import ndb
import logging

APP_KEY_TEMPLATE = '{}-{}'
FUNC_KEY_TEMPLATE = '{}-{}-{}'

class ApplicationReportEntry(ndb.Model):
    name = ndb.StringProperty()
    count = ndb.IntegerProperty(default=0)
    date = ndb.DateProperty()
    @classmethod
    def build_id(cls,name, date):
        return APP_KEY_TEMPLATE.format(name,date)
    @classmethod
    def getEntriesByDate(cls, date):
        qdate = date.replace(hour=00,minute=00, second = 00, microsecond= 00)
        logging.debug("Selecting Application entries from %s ", qdate.strftime("%Y-%m-%d %H:%M:%S"))
        return cls.query().filter(cls.date == qdate).order(-cls.count)



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
    def getEntriesLastHours(cls, hours):
        now = datetime.today()
        now = now.replace(minute=00, second = 00, microsecond= 00)
        past = now - timedelta(hours=hours)
        return cls.query().filter(cls.date == past).order(-cls.total)


    def setAccumulated(self, q):
        self.total = self.count + q
    def setCount(self, q):
        accumulated=self.total - self.count
        self.count = q
        self.setAccumulated(accumulated)