#!/usr/bin/env python3

'''
Get METAR data.

Usage: metar.py <ICAO> [<time>] [<timeEnd>] [-r | --raw] [--help | -h]

Options:

-h --help  Show help screen and exit.
-r --raw   Output raw METAR data.
'''

import logging
from docopt import docopt

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

# Get arguments and options from CLI as dict
args = docopt(__doc__)

# Store values
icao = args['<ICAO>'].upper()
time = [args['<time>'], args['<timeEnd>']]
raw = args['--raw']

logging.debug('Given ICAO is %s and raw ouput is %s' % (icao, raw))

# Check if a single time, time range, or no times given
if None not in time:
    logging.debug('A time range was provided: {}'.format(time))
elif time[0] is not None:
    logging.debug('A single time was given: {}'.format(time[0]))
else:
    logging.debug('No time given: {}'.format(time))
