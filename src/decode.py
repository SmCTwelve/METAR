#!/usr/bin/env python3

'''
Decode XML response.

Use an Element Tree structure to parse the XML and access tags, attributes
and values to be used for output. Match values with RegEx objects to determine
appropriate conditions.
'''

import xml.etree.ElementTree as ET
import dateutil.parser
import request


def trans(text):
    translation = {
        "MVFR": "Marginal VFR",
        "-RA": "Light rain",
        "RA": "Rain",
        "+RA": "Heavy rain",
        "TS": "Thunderstorm",
        "-SN": "Light snow",
        "SN": "Snow",
        "+SN": "Heavy snow",
        "CB": "Cumulonibus",
        "TCU": "Towering cumulus",
        "NSC": "No significant weather",
        "CLR": "Clear",
        "SKR": "Clear",
        "FEW": "Few clouds",
        "BKN": "Broken clouds",
        "SCT": "Scattered clouds",
        "OVC": "Overcast clouds"
    }
    return translation.get(text, "")


def display(data):

    print("METAR for {icao}".format(data["icao"]))
    print(data["date"])
    print()
    print("Conditions: {cond} \t {wx}.".format(
        data["cond"],
        data["wx"]))
    print("Wind {dir} degrees at {kt} knots.".format(
        data["wind"][0],
        data["wind"][1]), end='\t')
    print("Temperature: {c}C".format(data["temp"]), end='\t')
    print("Visibility: {vis}".format(data["vis"]))
    print("Sky conditions:")
    print("\tBase\t {cover} \t {alt}".format(
        data["clouds"]["base"][0],
        data["clouds"]["base"][1]))
    print("\tCeiling\t {cover}", "{alt}".format(
        data["clouds"]["ceiling"][0],
        data["clouds"]["ceiling"][1]))
    print("QNH", "{QNH}".format(data["QNH"]))
    print()


def parse(xml):
    '''
    Parse XML data as Element Tree and store values.

    :param xml: -- the string of XML data.
    '''
    tree = ET.fromstring(xml)
    root = tree.find("data")

    for metar in root.iterfind("METAR"):

        date = dateutil.parser.parse(metar.findtext("observation_time"))
        conditions = trans(metar.findtext("flight_category"))
        # Translate list of WX remakrs separated by spaces
        # Iterate over weather remarks and add translation to list
        weatherstring = metar.findtext("wx_string").split(" ")
        wx = []
        for weather in range(len(weatherstring)):
            wx.append(trans(weather))
        # Get all cloud reports as list
        cloudReports = metar.findall("sky_condition")
        # Base and ceiling layers cover and height as dict
        clouds = {
          "base": [
              trans(cloudReports[0].get("sky_cover")),
              cloudReports[0].get("cloud_base_ft_agl")
          ],
          "ceiling": [
            trans(cloudReports[len(cloudReports) - 1].get("sky_cover")),
            cloudReports[len(cloudReports) - 1].get("cloud_base_ft_agl")
          ]
        }
        # List of wind direction and speed
        wind = [
            metar.findtext("wind_dir_degrees"),
            metar.findtext("wind_speed_kt")
        ]
        QNH = metar.findtext("sea_level_pressure_mb")
        vis = metar.findtext("visibility_statute_mi")

        data = {
            "icao": metar.findtext("station_id"),
            "date": date.strftime("%a %b %Y, %X"),  # Thu 24 Aug, 21:00
            "cond": conditions,
            "temp": metar.findtext("temp_c"),
            "wx": wx,
            "clouds": clouds,
            "wind": wind,
            "QNH": QNH,
            "vis": vis
        }
        print(data)
        print(data.keys())
        display(data)



parse(request.metar("EGPF", mostRecent=True))

# Airport {ICAO}
# {Date and Time}
#
# Flight conditions: {condition}
# Wind {dir} at {speed}. Temperature {temp}. Sky condition {alt}ft {coverage}.
# QNH {mb}. Visibility {vis}.