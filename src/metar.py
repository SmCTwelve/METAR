#!/usr/bin/env python3

'''
Get METAR data.

Usage: metar.py <ICAO> [<startTime> <endTime>] [-r | --raw] [--help | -h]

Options:

-h --help  Show help screen and exit.
-r --raw   Output raw METAR data.
'''

import sys
import logging
from docopt import docopt

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

# Get arguments and options as dictionary
args = docopt(__doc__)

# Store values
icao = args['<ICAO>'].upper()
startTime = args['<startTime>']
endTime = args['<endTime>']
raw = args['--raw']
print(args)

logging.debug('Given ICAO is %s and raw ouput is %s' % (icao, raw))

if (startTime is None and endTime is None):
    logging.debug('No time range provided, using most recent time.')
    sys.exit()
elif (startTime is None or endTime is None):
    print('Start and end time required; leave blank for most recent METAR.')
else:
    logging.debug('Getting all METARS between {} and {}'.format(startTime, endTime))
