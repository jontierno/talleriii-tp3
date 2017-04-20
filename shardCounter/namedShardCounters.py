import generalCounterShardConfig as shard

FUNCTION_NAME_TEMPLATE = 'f-{}-{}-{}'
APPLICATION_NAME_TEMPLATE = 'a-{}-{}'

class FunctionCounter(shard.GeneralCounterShard):
	@classmethod
	def increment(cls,name, timestamp):
		namesh = FUNCTION_NAME_TEMPLATE.format(name, "%s/%s/%s" % (timestamp.day, timestamp.month, timestamp.year), timestamp.hour)
		shard.increment(namesh)


class ApplicationCounter(shard.GeneralCounterShard):
	@classmethod
	def increment(cls,name, timestamp):
		namesh = APPLICATION_NAME_TEMPLATE.format(name, "%s/%s/%s" % (timestamp.day, timestamp.month, timestamp.year))
		shard.increment(namesh)