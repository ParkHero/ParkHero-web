__author__ = 'abertschi'
from livedata.zurich_live_get import ZurichLiveGet


class LiveGetCollection(object):

    def __init__(self):
        self.collection = []
        self.collection.append(ZurichLiveGet())
        pass

    def get_all(self):
        result = []
        for live in self.collection:
            result.extend(live.get_all())
        return result
