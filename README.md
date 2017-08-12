# METAR
Request and decode [METAR](https://en.wikipedia.org/wiki/METAR) weather data with multiple options. 

## DESCRIPTION
This simple program will display the METAR for an airport, or range of airports, by specifying the [ICAO](https://en.wikipedia.org/wiki/International_Civil_Aviation_Organization_airport_code). An optional timestamp can be used to get the weather for a specific time, or if two timestamps are present all METARs between the first and last time will be shown.

Uses the NOAA [Aviation Weather Center's](https://www.aviationweather.gov/metar?gis=off) ADDS API for requests.  

## Usage
To get the current METAR for KLAX:
```
metar KLAX
```
By default the program will decode the METAR and output a simplified description of the conditions. The raw METAR can be viewed with the `-raw` or `-r` flag. 

