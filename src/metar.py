#!/usr/bin/env python3

'''
\r\nGet METAR data.

Usage: metar.py <ICAO> [<startTime> <endTime>] [-r | --raw] [--help | -h]

Options:

-h --help  Show help screen and exit.
-r --raw   Output raw METAR data.

Details:

An optional time range may be provided to return all METARs (up to 3 days)
between the start and end times. If omitted, the most recent METAR within the
past hour will be requested. A date and time must be quoted as a string.

Examples:
* metar.py KLAX "2017-08-18 11:00:00" "2017-08-20 16:30:00"
* metar.py KLAX 11:00 21:00
* metar.py KLAX "08 11:00" "10 21:00" --raw
* metar.py KLAX 11h 13h
* metar.py KLAX
\r\n
'''

import sys
import logging
import request
from docopt import docopt

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

# Get arguments and options as dictionary
args = docopt(__doc__)

# Store values
icao = args['<ICAO>'].upper()
startTime = args['<startTime>']
endTime = args['<endTime>']
raw = args['--raw']

print()
logging.debug('Given ICAO is %s and raw ouput is %s' % (icao, raw))

# Send data to request.py
if (startTime is None and endTime is None):
    # No time range provided, request most recent
    logging.debug('No time range provided, using most recent time.')
    request.metar(icao)
elif (startTime is None or endTime is None):
    # A single time given when both required, exit
    print('Start and end time required; leave blank for most recent METAR.')
    sys.exit()
else:
    # Both start and end times given, request within range
    logging.debug('Getting all METARS between {} and {}'.format(startTime, endTime))
    request.metar(icao, startTime, endTime, mostRecent=False)
