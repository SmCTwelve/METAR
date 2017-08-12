#! usr/bin/python3

'''
Get METAR data for the specified ICAO or range of ICAO's for the current
time, or a specified timestamp or range. Use input to request METAR from
ADDS aviation weather database API. Optionally parse and decode the METAR
for a simplied output describing the conditions, or default to a raw data
output for each request.

Usage: metar.py <ICAO> [<time>, [<timeEnd>]] [-decode, -d] [-help, -h]
'''

