#!/usr/bin/env python3

'''
Decode XML response.

Use an Element Tree to parse the XML and access tags, attributes
and values to be used for output. Match values with RegEx to provide
translations for appropriate conditions.
'''

import xml.etree.ElementTree as ET
import dateutil.parser
import re
import logging


logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


def trans(text):
    '''
    Match input text with dictionary key for translated value.

    :param text: -- string to be translated.
    :return: -- translated string, or empty string if no match.
    '''
    translation = {
        ("VFR", "VMC"): "VFR",
        ("MVFR",): "Marginal",
        ("IFR", "IMC"): "IFR",
        ("RA",): "Rain",
        ("SN", "SG"): "Snow",
        ("TS",): "Thunderstorm",
        ("CB",): "Cumulonibus",
        ("TSRA",): "Rain and thunderstorm",
        ("TCU",): "Towering cumulus",
        ("NSC", "NOSIG"): "No significant weather",
        ("CLR", "SKR"): "Clear",
        ("FEW",): "Few",
        ("BKN",): "Broken",
        ("SCT",): "Scattered",
        ("OVC",): "Overcast",
        ("FG",): "Fog",
        ("HZ",): "Haze",
        ("IC", "GR", "GS", "PL"): "Hail/Ice",
        ("DZ",): "Drizzle",
        ("FZ",): "Freezing",
        ("SA", "PO"): "Dust/Sand",
        ("DS", "SS"): "Sandstorm",
        ("VA",): "Volcanic ash",
        ("SH",): "Showers",
        ("VC",): "in vincinity",
    }
    matches = []
    if text.startswith("+"):
        matches.append("Heavy")
        text = text.lstrip("+")
    if text.startswith("-"):
        matches.append("Light")
        text = text.lstrip("-")
    for keys, value in translation.items():
        for k in keys:
            if k == text:
                matches.append(value)
    return " ".join(matches)


def display(data, raw):
    '''
    Present the METAR data as formatted output.

    :param raw: -- display raw text if true.
    :param data: -- dictionary with decoded data.
    '''
    print()
    print('-' * 100)

    # Header
    print("METAR for {}"
          .format(data["icao"]))
    print(data["date"])
    print()

    # Show raw text if requested
    if (raw is True):
        print(data["raw"])
    else:
        # Conditions summary
        print("Conditions: {} -- {}"
              .format(
                  data["cond"],
                  "; ".join(data["wx"]))
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
        print("Pressure:", "{}".format(data["QNH"]))
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


def parse(xml, raw):
    '''
    Parse XML data and store values.

    Construct an Element Tree from XML and iterate over each METAR section.
    Parse the values of the required elements and store them, translating them
    if required. The final data, including translated text, is placed into a
    dictionary to be accessed during output.

    :param xml: -- the string of XML data to be parsed.
    :param raw: -- if the raw METAR text should be displayed.
    :return data: -- dict of decoded data.
    '''
    tree = ET.fromstring(xml)
    root = tree.find("data")

    logging.debug("Parsing XML...")

    # Iterate over each METAR returned
    for metar in root.iterfind("METAR"):
        date = dateutil.parser.parse(metar.findtext("observation_time"))
        conditions = trans(metar.findtext("flight_category"))

        # Translate weather remarks, if present
        if metar.find("wx_string") is not None:
            # Split weather remarks into list of individual strings
            weatherStringList = metar.findtext("wx_string").split(" ")
            wx = []
            # Translate each weather string and append to list
            for weather in weatherStringList:
                wx.append(trans(weather))
        # If no weather remarks use empty string
        else:
            wx = [trans("NOSIG")]

        # Get all cloud report elements as list
        cloudReports = metar.findall("sky_condition")
        # Store base and ceiling cover and altitude as dict
        # Ceiling is last cloud report in list, base is first
        if (len(cloudReports) > 0):
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

        else:
            clouds = {
                "base": ["Clear", "None"],
                "ceiling": ["Clear", "None"]
            }
        # Store wind direction and speed
        wind = [
            metar.findtext("wind_dir_degrees"),
            metar.findtext("wind_speed_kt")
        ]

        # Get QNH, if tag not present match it from the raw text string
        # Search for AXXXX or QXXXX
        QNH = re.search(r"([QA]\d{4})", metar.findtext("raw_text")).group()
        if ("A" in QNH):
            # If Altimeter, strip letter and add decimal; e.g. 29.92
            QNH = QNH[1:3] + "." + QNH[3:] + " inHg"
        else:
            # Else using QNH, strip letter
            QNH = QNH.lstrip("Q") + " mb"

        # Get visibility
        vis = metar.findtext("visibility_statute_mi")

        # Raw metar string
        rawtext = metar.findtext("raw_text")

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
            "vis": vis,
            "raw": rawtext
        }
        # Display the current METAR
        display(data, raw)
