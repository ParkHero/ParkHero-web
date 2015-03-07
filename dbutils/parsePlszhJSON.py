__author__ = 'leo'

import json



def run():
    json_dump = open('../data/parkhaus.json')

    data = json.load(json_dump)
    sqlf = open("../data/parkhaus.sql", "w+")

    sqlf.write("DROP TABLE IF EXISTS t_parkhaus; \r\n")
    sqlf.write("CREATE TABLE t_parkhaus ("
               "pid INT autoincrement,"
               "name TEXT,"
               "slots INT,"
               "free_slots INT,"
               "longitude FLOAT,"
               "latitude FLOAT,"
               "address TEXT);\r\n")


    sqlf.write("INSERT INTO t_parkhaus (name, slots, free_slots, longitude, latitude, address) VALUES ")

    for phfeature in data['features']:
        props = phfeature['properties']
        longitude = phfeature['geometry']['coordinates'][0]
        latitude = phfeature['geometry']['coordinates'][1]

        sqlf.write("(\"{0}\", {1}, {2}, {3}, {4}, \"{5}\"), \r\n".format(
                        props['Name'], props['oeffentlich'], props['oeffentlich'],
                        longitude, latitude, props['Adresse']))

    json_dump.close()
    sqlf.close()

if __name__ == "__main__":
    run()