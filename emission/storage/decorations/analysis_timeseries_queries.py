import logging
import pymongo

import emission.storage.timeseries.timequery as estt

import emission.core.wrapper.entry as ecwe
import emission.storage.timeseries.abstract_timeseries as esta

RAW_TRIP_KEY = "segmentation/raw_trip"
RAW_PLACE_KEY = "segmentation/raw_place"
RAW_SECTION_KEY = "segmentation/raw_section"
RAW_STOP_KEY = "segmentation/raw_stop"
CLEANED_TRIP_KEY = "analysis/cleaned_trip"
CLEANED_PLACE_KEY = "analysis/cleaned_place"
CLEANED_SECTION_KEY = "analysis/cleaned_section"
CLEANED_STOP_KEY = "analysis/cleaned_stop"
CLEANED_LOCATION_KEY = "analysis/recreated_location"

# General methods

def get_object(key, object_id):
    return get_entry(key, object_id).data

def get_entry(key, object_id):
    return esta.TimeSeries.get_aggregate_time_series().get_entry_from_id(
        key, object_id)

def get_objects(key, user_id, time_query, geo_query=None):
    return [entry.data for entry in
            get_entries(key, user_id=user_id, time_query=time_query,
                        geo_query=geo_query)]

def get_entries(key, user_id, time_query, geo_query=None,
                extra_query_list=None):
    if user_id is not None:
        ts = esta.TimeSeries.get_time_series(user_id)
    else:
        ts = esta.TimeSeries.get_aggregate_time_series()
    doc_cursor = ts.find_entries([key], time_query, geo_query, extra_query_list)
    # TODO: Fix "TripIterator" and return it instead of this list
    curr_entry_list = [ecwe.Entry(doc) for doc in doc_cursor]
    logging.debug("Returning entry with length %d result" % len(curr_entry_list))
    return curr_entry_list

def get_aggregate_places(key, time_query, geo_query=None):
    result_cursor = esta.TimeSeries.get_aggregate_time_series().find_entries(
        key_list=["data.location"], time_query=time_query)
    return [ecwe.Entry(doc).data for doc in result_cursor]

# Object-specific associations


def get_time_query_for_trip_like(key, trip_like_id):
    """
    Returns the query that returns all the points associated with this
    trip-like (raw trip, cleaned trip, raw section) 
    """
    trip = get_object(key, trip_like_id)
    return estt.TimeQuery("data.ts", trip.start_ts, trip.end_ts)

