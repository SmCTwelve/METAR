#!/usr/bin/env python3

'''
Request METAR data.

API takes the following parameters:

* ``stationString`` -- the ICAO for the METAR request
* ``startTime`` -- time and date (3 days) to specify the start of time range.
* ``endTime`` -- specifies end of date time range.
* ``mostRecent`` -- returns most recent METAR (default if no start or end time)
'''

import logging
import requests
import dateutil.parser

#########
# TO DO #
#########
# Better interpretation of time values e.g. 1100, 1100h, 11
# Interpret time first rather than date or year
# Write custom RegEx date parser for above formats instead of dateutil
# Handle multiple ICAO arguments

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')


def getDateTime(time):
    '''
    Convert given times to ISO8601 date time format.

    :param time: The time string to be converted.
    :return: The converted date string.
    '''
    dateObj = dateutil.parser.parse(time)
    return dateObj.strftime('%Y-%m-%dT%H:%M:%SZ')


def makeQuery(icao, startTime, endTime, mostRecent):
    '''
    Construct API query using parameter values.

    If no time range is given the most recent METAR is requested.

    :param icao: -- The airport to get METAR from.
    :param startTime: -- Beginning of time range.
    :param endTime: -- End of time range.
    :param mostRecent: -- Whether the most recent METAR should be
    fetched.

    :return: -- The query string. ``ICAO + start + end`` or ``ICAO + recent``
    '''
    station = '&stationString=%s' % (icao)
    # No times given, use most recent METAR
    if (mostRecent):
        query = url + station + '&mostRecent=True' + '&hoursBeforeNow=1'
    # Use the provided time range
    else:
        start = '&startTime=%s' % (getDateTime(startTime))
        end = '&endTime=%s' % (getDateTime(endTime))
        query = url + station + start + end
    logging.debug(query)
    return query


def getResponse(query):
    '''
    Attempt to fetch METAR using provided query.

    Check response status and raise exception if error. Response text
    stored and returned.

    :param query: The query string to append to the API request.

    :return: Raw text from the GET response.
    '''
    res = requests.get(query)
    res.raise_for_status()
    logging.debug(res)
    return res


def metar(icao, startTime=None, endTime=None, mostRecent=True):
    '''
    Request METAR from API.

    The :param icao: is required. Optional :startTime: and
    :endTime: may be provided to return all METARs within the range.
    If no times are given the :mostRecent: will be used, which
    defaults to ``True`` if no other parameters are given.
    '''
    text = getResponse(makeQuery(icao, startTime, endTime, mostRecent)).text
    return text


# API request url; append params
url = ('https://www.aviationweather.gov/adds/dataserver_current/httpparam?'
       'dataSource=metars&requestType=retrieve&format=xml')
