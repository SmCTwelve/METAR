## METAR
Request and decode [METAR](https://en.wikipedia.org/wiki/METAR) weather data with multiple options.

#### DESCRIPTION
This simple program will display the METAR for an airport, or range of airports (such as the departure and arrival airports) by specifying the [ICAO](https://en.wikipedia.org/wiki/International_Civil_Aviation_Organization_airport_code). An optional time range can be given to get the weather for a specific time. The program can parse the raw METAR and translate it into a formatted output in plain English describing the conditions for ease of use in flight planning.

Uses the NOAA [Aviation Weather Center's](https://www.aviationweather.gov/metar?gis=off) ADDS API for requests.

#### USAGE
```
py metar.py <ICAO> [<start> <end>] [--raw] [--help]
```
By default the program will decode the METAR and output a simplified description of the conditions. The raw METAR text can be viewed with the `--raw` or `-r` flag.

An optional time range may be provided (up to 3 days old) to see all METAR reports between the `start` and `end` times. This accepts many formats shown in the examples below. Note that when providing both a date and a time, it must be quoted in a single string.

If the request is valid the program will display the results in the output window. This includes a header with the ICAO, date and time of the current METAR. This is followed by a summary of the conditions, such as VFR/IFR and any significant weather remarks. The wind, temperature, visibility and atmospheric pressure is also shown, in the correct format depending on region (inHg in the US, millibars elsewhere). Finally, a summary of the sky conditions is given, with the cloud cover and alititude for the base and ceiling layers (if present).

#### EXAMPLES

To get the current metar for KLAX - Los Angeles:

```
py metar.py KLAX
```

This will automatically request the most recent METAR from the past hour if no other parameters are provided.

To request all METARs between 11AM and 3PM today:

```
py metar.py KLAX 11:00 15:00
```

To only see the `--raw` METAR text between 08 Aug, 3PM and 10 Aug, 12PM:

```
py metar.py KLAX "08 Aug 15:00" "10 Aug 12:00"
```

More examples:

```
py metar.py KLAX 11h 12h
py metar.py KLAX "08 11:00" "08 15:00"
py metar.py KLAX "2017-08-18 11:00:00" "2017-08-20 16:30:00" --raw
```

#### OUTPUT

Requesting the `--raw` text will simply provide the METAR string straight from the API.
```
py metar.py KLAX --raw
```

will return

>KLAX 292253Z 25010KT 9SM FEW100 FEW150 26/19 A2975 RMK AO2 SLP073 T02610189

Which can result in a decoded output:

```
---------------------------------------------------------------------------------------------------
METAR for KLAX
Tue Aug 2017, 22:53:00

Conditions: VFR --
Wind: 250 degrees at 10 kts   Temperature: 26.1C    Visibility: 9.0sm     Pressure: 29.75 inHg
---------------------------------------------------------------------------------------------------
Sky conditions:
                        CLOUD     ALT (FT)
        BASE              Few        10000
        CEILING           Few        15000
```
