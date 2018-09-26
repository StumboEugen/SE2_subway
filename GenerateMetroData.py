# -*- coding: UTF-8 -*-

# This Script is used to decode the html file which contains the
# lines and stations of Shanghai metro.
# The data is saved in a json file formating like: MetroData_Example.json.

import os
import codecs
import json
from bs4 import BeautifulSoup

import Utility

# constant
LINE_COLOR = {
    "1": "#e91b39",
    "2": "#8ac53f",
    "3": "#fad107",
    "4": "#502e8d",
    "5": "#9056a3",
    "6": "#d61870",
    "7": "#f37121",
    "8": "#009eda",
    "9": "#79c8ed",
    "10": "#bca8d1",
    "11": "#7e2131",
    "12": "#007c65",
    "13": "#e895c0",
    "16": "#8dd1bf"
}
PATH_NOW = os.path.dirname(__file__)
SRC_FILE_PATH = PATH_NOW + "//MetroData_SH.html"
RLT_FILE_PATH = PATH_NOW + "//MetroData_SH.json"


# Start of main()
def main():
    metrodata = {"line":[], "station":[], "route":[]}
    
    # read form file.
    with codecs.open(SRC_FILE_PATH, encoding="utf-8") as fp:
        str_htmlsrc = fp.read()

    # initialize the decoder.
    htmldecoder = BeautifulSoup(str_htmlsrc, "html.parser")

    # find all stations and route in Shanghai Metro.
    stations = htmldecoder.find_all("circle", {"class": "station"})
    routes = htmldecoder.find_all("line", {"class": "route"})

    # generate json data.
    # generate station data.
    for _iterator, _station in enumerate(stations):
        _dict_station = {}
        _dict_station["stationName"] = _station["id"]
        _dict_station["stationID"] = _iterator
        _dict_station["stationPos"] = {"posX":_station["cx"],"posY":_station["cy"]}
        _dict_station["transferLine"] = []
        _dict_station["nextStationID"] = []
        metrodata["station"].append(_dict_station)

    # generate route data.
    for _iterator, _route in enumerate(routes):
        # generate route data.
        _dict_route = {}
        _routeName = _route["id"]
        _routeEntry = _routeName.split("-")
        _routeEntryID = []
        _routeEntryID.append(Utility.find(metrodata["station"], _routeEntry[0],
            keyfunc=lambda x: x["stationName"])["stationID"])
        _routeEntryID.append(Utility.find(metrodata["station"], _routeEntry[1],
            keyfunc=lambda x: x["stationName"])["stationID"])
        _routeColor = _route["stroke"]
        _routeStart = {"posX":_route["x1"], "posY":_route["y1"]}
        _routeEnd = {"posX":_route["x2"], "posY":_route["y2"]}
        _routeLineID = [int(k) for k, v in LINE_COLOR.items() if v == _routeColor].pop()
        # fill in the dictionary represent a route.
        _dict_route["routeName"] = _routeName
        _dict_route["routeEntry"] = _routeEntry
        _dict_route["routeEntryID"] = _routeEntryID
        _dict_route["routeColor"] = _routeColor
        _dict_route["routeStart"] = _routeStart
        _dict_route["routeEnd"] = _routeEnd
        _dict_route["routeLineID"] = _routeLineID
        # fill "adjacentStation" in station
        metrodata["station"][_routeEntryID[0]]["nextStationID"].append(_routeEntryID[1])
        metrodata["station"][_routeEntryID[1]]["nextStationID"].append(_routeEntryID[0])
        # fill in metrodata json object.
        metrodata["route"].append(_dict_route)

    # generate line data.
    for _linenumber in LINE_COLOR:
        _dict_line = {}
        # fill in the dictionary represent a line.
        _dict_line["lineName"] = "Line_" + _linenumber
        _dict_line["lineID"] = int(_linenumber)
        _dict_line["lineStation"] = []
        _dict_line["lineStationID"] = []
        _dict_line["lineColor"] = LINE_COLOR[_linenumber]
        # fill in metrodata json object.
        metrodata["line"].append(_dict_line)

    # fill in "lineStation" & "lineStationID" in line data.
    for _route in metrodata["route"]:
        _routeEntryID = _route["routeEntryID"]
        _routeEntry = _route["routeEntry"]
        _routeLineID = _route["routeLineID"]
        _routeLine = Utility.find(metrodata["line"], _routeLineID,
            keyfunc = lambda x: x["lineID"])
        if (not _routeEntryID[0] in _routeLine["lineStationID"]):
            _routeLine["lineStationID"].append(_routeEntryID[0])
            _routeLine["lineStation"].append(_routeEntry[0])
        if (not _routeEntryID[1] in _routeLine["lineStationID"]):
            _routeLine["lineStationID"].append(_routeEntryID[1])
            _routeLine["lineStation"].append(_routeEntry[1])

    # fill in "transferLine" in station data.
    for _line in metrodata["line"]:
        for _stationid in _line["lineStationID"]:
            metrodata["station"][_stationid]["transferLine"].append(_line["lineID"])

    # convert python dictionary to json string.
    str_json_metrodata = json.dumps(metrodata, ensure_ascii=False)

    # write to json file
    with codecs.open(RLT_FILE_PATH, mode="w", encoding="utf-8") as fp:
        fp.write(str_json_metrodata)
    
    print("Convert finished!")
    return 0
# End of main()


if __name__ == "__main__":
    main()