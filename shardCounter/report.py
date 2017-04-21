import datetime

from google.appengine.ext import ndb


KEY_TEMPLATE = '{}-{}'


class ApplicationReportEntry(ndb.Model):
    name = ndb.StringProperty()
    count = ndb.IntegerProperty(default=0)
    date = ndb.DateProperty()
    @classmethod
    def build_id(cls,name, date):
        return KEY_TEMPLATE.format(name,date)
