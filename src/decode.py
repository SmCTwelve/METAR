#!/usr/bin/env python3

'''
Decode XML response.

Use an Element Tree to parse the XML and access tags, attributes
and values to be used for output. Match values with RegEx to provide
translations for appropriate conditions.
'''

import xml.etree.ElementTree as ET
import dateutil.parser
import request
import re

# ## TO DO ##
# Display raw out
# Integrate with main app
# Refactor and clean up


def trans(text):
    '''
    Match input text with dictionary key for translated value.

    :param text: -- string to be translated.
    :return: -- translated string, or empty string if no match.
    '''
    translation = {
        "MVFR": "Marginal VFR",
        "VFR": "VFR",
        "IFR": "IFR",
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
        "NOSIG": "No significant weather",
        "CLR": "Clear",
        "SKR": "Clear",
        "FEW": "Few",
        "BKN": "Broken",
        "SCT": "Scattered",
        "OVC": "Overcast",
        "VCTS": "Thunderstorms in the vicinity",
        "VC": "Vicinity",
        "TSRA": "Thunderstorm and rain",
        "-TSRA": "Thunderstorm and light rain",
        "+TSRA": "Thunderstorm and heavy rain"
    }
    matches = re.search(" ".join(translation.keys()), "[{}]".format(text))
    print("Matches {}".format(matches))
    return translation.get(text, "")


def display(data):
    '''
    Present the METAR data as formatted output.
    :param data: -- dictionary with decoded data.
    '''

    print()
    print('-' * 100)

    # Header
    print("METAR for {}"
          .format(data["icao"]))
    print(data["date"])
    print()

    # Conditions summary
    print("Conditions: {} -- {}"
          .format(
            data["cond"],
            " ".join(data["wx"]))
          )

    # Wind, temp, visibility, pressure
    print("Wind: {} degrees at {} kts"
          .format(
            data["wind"][0],
            data["wind"][1]
          ), end='\t')
    print("Temperature: {}C"
          .format(data["temp"]), end='\t')
    print("Visibility: {}sm"
          .format(data["vis"]), end='\t')
    print("QNH:", "{}".format(data["QNH"]))
    print('-' * 100)

    # Sky condition, base and ceiling cloud layers
    print("Sky conditions:")
    print("\t {:>20} {:>12}".format("CLOUD", "ALT (FT)"))
    print("\tBASE\t {:>12} {:>12}"
          .format(
            data["clouds"]["base"][0],
            data["clouds"]["base"][1])
          )
    print("\tCEILING\t {:>12} {:>12}"
          .format(
            data["clouds"]["ceiling"][0],
            data["clouds"]["ceiling"][1])
          )
    print()


def parse(xml):
    '''
    Parse XML data and store values.

    Construct an Element Tree from XML and iterate over each METAR section.
    Parse the values of the required elements and store them, translating them
    if required. The final data, including translated text, is placed into a
    dictionary to be accessed during output.

    :param xml: -- the string of XML data to be parsed.
    :return data: -- dict of decoded data.
    '''
    tree = ET.fromstring(xml)
    root = tree.find("data")

    # Iterate over each METAR returned
    for metar in root.iterfind("METAR"):
        date = dateutil.parser.parse(metar.findtext("observation_time"))
        conditions = trans(metar.findtext("flight_category"))

        # Translate weather remarks, if present
        if (metar.find("wx_string") is not None):
            # Split weather remarks into list of individual strings
            weatherstring = metar.findtext("wx_string").split(" ")
            wx = []
            # Translate each weather string and append to list
            for weather in range(len(weatherstring)):
                wx.append(trans(weatherstring[weather]))
        # If no weather remarks use empty string
        else:
            wx = ""

        # Get all cloud report elements as list
        cloudReports = metar.findall("sky_condition")
        # Store base and ceiling cover and altitude as dict
        # Ceiling is last cloud report in list, base is first
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
        # Use empty strings if no alts given
        if (clouds["base"][1] is None):
            clouds["base"][1] = ""
        if (clouds["ceiling"][1] is None):
            clouds["ceiling"][1] = ""

        # Store wind direction and speed
        wind = [
            metar.findtext("wind_dir_degrees"),
            metar.findtext("wind_speed_kt")
        ]

        # Get QNH, if tag not present match it from the raw text string
        if (metar.findtext("sea_level_pressure_mb") is not None):
            QNH = metar.findtext("sea_level_pressure_mb")
        else:
            # Search for AXXXX or QXXXX
            QNH = re.search(metar.findtext("raw_text"),
                            "([Q]\d{4})|([A]\d{4})")

        # Get visibility
        vis = metar.findtext("visibility_statute_mi")

        # Final data for output
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
    display(data)
    return data



parse(request.metar("KIAH"))
