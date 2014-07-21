# This script is a simple MapReduce implementation
# of creating an inverse index where each word
# is linked to a list of document ids that contain it

import MapReduce
import sys

# Part 1: create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: emit word:document_id pairs avoiding duplicates
def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = set(value.split())  ## removes duplicates
    for w in words:
      mr.emit_intermediate(w, key)

# Part 3: remove duplicates from list_of_ids and emit it
def reducer(key, list_of_ids):
    # key: word
    # value: list of occurrence counts
    list_of_ids = list(set(list_of_ids))  ## remove duplicates again
    mr.emit((key, list_of_ids))

# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)
