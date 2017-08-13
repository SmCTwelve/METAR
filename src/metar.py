#!/usr/bin/env python3

'''
Get METAR data.

Usage: metar.py <ICAO> [<time>] [<timeEnd>] [-r | --raw] [--help | -h]

Options:

-h --help  Show help screen and exit.
-r --raw   Output raw METAR data.
'''

from docopt import docopt

# Get arguments and options as dict
args = docopt(__doc__)

# Store values
icao = args['<ICAO>']
time = [args['<time>'], args['<timeEnd>']]
raw = args['--raw']
