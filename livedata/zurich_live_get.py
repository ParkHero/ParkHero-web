from urllib.request import urlopen
from bs4 import BeautifulSoup
from livedata import *

URL = "http://www.plszh.ch/plsFeed/rss"

class ZurichLiveGet(LiveGet):


    def __init__(self):
        pass

    def get_by_name(self, name):
        for house in self.get_all():
            if house.name.lower() == name.lower():
                return house
        return None

    def get_all(self):
        content = urlopen(URL).read()
        results = []
        soup = BeautifulSoup(content)
        for item in soup.rss.channel.find_all('item'):
            parkhouse = ParkhouseLiveData()

            # parkhaus name
            # i.e. Parkhaus Hauptbahnhof / Sihlquai 41
            name = item.title.string.split("/")
            if (len(name) > 1):
                name = name[0].replace("Parkhaus", "").replace("Parkplatz", "").strip()
                parkhouse.name = name
            else:
                parkhouse.name = name.string

            # open state and amount
            descList = item.description.string.split("/")
            state = descList[0].strip()
            free = descList[1].strip()
            if state == "open":
                parkhouse.open = True
                parkhouse.free = free
            else:
                parkhouse.open = False
                parkhouse.free = 0

            results.append(parkhouse)
        return results


if __name__ == "__main__":
    print(ZurichLiveGet().get_by_name('Accu'))


