import generalCounterShardConfig as shard
import report
from google.appengine.ext import ndb
import logging
from datetime import datetime, timedelta
FUNCTION_NAME_TEMPLATE = '{}-{}-{}'
APPLICATION_NAME_TEMPLATE = '{}-{}'
REPORT_HOURS= 12


class FunctionCounter(shard.GeneralCounterShard):
	@classmethod
	def increment(cls,name, timestamp):
		namesh = FUNCTION_NAME_TEMPLATE.format(name, "%s/%s/%s" % (timestamp.day, timestamp.month, timestamp.year), timestamp.hour)
		shard.increment(FunctionCounter,namesh)
	@classmethod
	def get_dirties(cls):
		return shard.GeneralCounterShardConfig.get_dirties(FunctionCounter)
	@classmethod
	def get_count(cls, name):
		return 1

	@classmethod
	def consolidate(cls, config):
		now = datetime.today()
		now = now.replace(minute=00, second = 00)
		past = now - timedelta(hours=REPORT_HOURS)
		
		#consolidating counter of the entry
		keyName=ndb.Key.id(config.key)
		split = keyName.split("-")
		functionName = split[0]
		functionDate = split[1]
		functionHour = split[2]
		date= datetime.strptime(functionDate + " " +functionHour, "%d/%m/%Y %H")
		count=shard.get_count(keyName,FunctionCounter)
		logging.info(keyName)
		entry = report.FunctionReportEntry.get_one(functionName,functionDate,functionHour)
		entry.setCount(count)
		entry.name=functionName
		entry.date=date
		entry.put()

		# i needn't update all, but it's a quick and dirty solution.
		accumulated = 0
		actualDate=now
		if past <= date:
			while actualDate > past:
				entry = report.FunctionReportEntry.get_one(functionName,"%s/%s/%s" % (actualDate.day, actualDate.month, actualDate.year), actualDate.hour)
				entry.setAccumulated(accumulated)
				entry.date = actualDate
				entry.name=functionName
				accumulated+=entry.count
				#TODO, i musn't create it in order to dont make delete
				if entry.total >0:
					entry.put()
				else:
					entry.key.delete()
				actualDate =  actualDate -timedelta(hours=1)

		config.dirty=False;
		config.put()


class ApplicationCounter(shard.GeneralCounterShard):
	@classmethod
	def increment(cls,name, timestamp):
		namesh = APPLICATION_NAME_TEMPLATE.format(name, "%s/%s/%s" % (timestamp.day, timestamp.month, timestamp.year))
		shard.increment(ApplicationCounter,namesh)
	@classmethod
	def get_dirties(cls):
		return shard.GeneralCounterShardConfig.get_dirties(ApplicationCounter)
	@classmethod
	def consolidate(cls, config):
		name=ndb.Key.id(config.key)
		split = name.split("-")
		applicationName=split[0]
		applicationDate = split[1]
		logging.info(split)
		date= datetime.strptime(applicationDate, "%d/%m/%Y")
		
		config.dirty=False;
		config.put()
		count=shard.get_count(name,ApplicationCounter)
		bId = report.ApplicationReportEntry.build_id(applicationName,applicationDate)
		entry = report.ApplicationReportEntry.get_or_insert(bId)
		entry.count = count
		entry.name=applicationName
		entry.date=date
		entry.put()
