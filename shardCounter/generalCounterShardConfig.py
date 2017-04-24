import random
import datetime
import logging
from google.appengine.api import memcache
from google.appengine.ext import ndb

SHARD_KEY_TEMPLATE = 'shard-{}-{:d}'


class GeneralCounterShardConfig(ndb.Model):
    """Tracks the number of shards for each named counter."""
    num_shards = ndb.IntegerProperty(default=30)
    kind = ndb.StringProperty()
    """Track if the counter is dirty"""
    dirty = ndb.BooleanProperty(default=False)
    lastDirty = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def all_keys(cls, name, kind):

        config = cls.get_or_insert(name)
        shard_key_strings = [SHARD_KEY_TEMPLATE.format(name, index)
                             for index in range(config.num_shards)]
        return [ndb.Key(kind, shard_key_string)
                for shard_key_string in shard_key_strings]

    @classmethod
    def get_dirties(cls, kind):
        logging.debug("Searching dirties for kind {}".format(kind.__name__))
        return cls.query().filter(cls.dirty == True,
                                  cls.kind == kind.__name__).order(
            cls.lastDirty)


class GeneralCounterShard(ndb.Model):
    """Shards for each named counter."""
    count = ndb.IntegerProperty(default=0)


def get_count(name, kind):
    total = memcache.get(name)

    if total is None:
        total = 0
        all_keys = GeneralCounterShardConfig.all_keys(name, kind)
        for counter in ndb.get_multi(all_keys):
            if counter is not None:
                total += counter.count
        memcache.add(name, total, 60)
    return total


def increment(kind, name):
    ##memcache.get(name)
    config = GeneralCounterShardConfig.get_or_insert(name)
    config.kind = kind.__name__
    _increment(kind, name, config.num_shards)
    _mark_dirty(config)


@ndb.transactional
def _mark_dirty(config):
    if not config.dirty:
        config.dirty = True
        config.put()


@ndb.transactional
def _increment(kind, name, num_shards):
    index = random.randint(0, num_shards - 1)
    shard_key_string = SHARD_KEY_TEMPLATE.format(name, index)
    counter = kind.get_by_id(shard_key_string)
    if counter is None:
        counter = kind(id=shard_key_string)
    counter.count += 1
    counter.put()
    # Memcache increment does nothing if the name is not a key in memcache
    memcache.incr(name)
