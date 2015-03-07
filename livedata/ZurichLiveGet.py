from urllib.request import urlopen
from bs4 import BeautifulSoup
from ParkhouseLiveData import ParkhouseLiveData

class ZurichLiveGet(object):
  _url = "http://www.plszh.ch/plsFeed/rss"
  
  def __init__(self):
    pass


  # get live data for parking house by name
  # return -1 if nothing found
  def getByName(self, name):
    for house in self.getAll():
      print(house.name)
      if house.name.lower() == name.lower():
        return house
    return -1

  def getAll(self):
    content = urlopen(self._url).read()
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
      if (descList[0].strip() == "open"):
        parkhouse.open = 1
      else:
        parkhouse.open = 0

      parkhouse.free = descList[1].strip()
      results.append(parkhouse)
    return results

if __name__ == "__main__":
  print(ZurichLiveGet().getByName('Accu'))


