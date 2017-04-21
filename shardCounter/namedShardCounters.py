import generalCounterShardConfig as shard
import report
from google.appengine.ext import ndb
import logging
from datetime import datetime
FUNCTION_NAME_TEMPLATE = '{}-{}-{}'
APPLICATION_NAME_TEMPLATE = '{}-{}'


class FunctionCounter(shard.GeneralCounterShard):
	@classmethod
	def increment(self,name, timestamp):
		namesh = FUNCTION_NAME_TEMPLATE.format(name, "%s/%s/%s" % (timestamp.day, timestamp.month, timestamp.year), timestamp.hour)
		shard.increment(FunctionCounter,namesh)
	@classmethod
	def get_dirties(self):
		return shard.GeneralCounterShardConfig.get_dirties(FunctionCounter)
	@classmethod
	def get_count(self, name):
		return 1

class ApplicationCounter(shard.GeneralCounterShard):
	@classmethod
	def increment(self,name, timestamp):
		namesh = APPLICATION_NAME_TEMPLATE.format(name, "%s/%s/%s" % (timestamp.day, timestamp.month, timestamp.year))
		shard.increment(ApplicationCounter,namesh)
	@classmethod
	def get_dirties(self):
		return shard.GeneralCounterShardConfig.get_dirties(ApplicationCounter)
	@classmethod
	def consolidate(self, config):
		name=ndb.Key.id(config.key)
		split = name.split("-")

		date= datetime.strptime(split[1], "%d/%m/%Y")

		config.dirty=False;
		config.put()
		count=shard.get_count(name,ApplicationCounter)
		bId = report.ApplicationReportEntry.build_id(name,split[1])
		entry = report.ApplicationReportEntry.get_or_insert(bId)
		entry.count = count
		entry.name=split[0]
		entry.date=date
		entry.put()
