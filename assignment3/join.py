# This script is a simple MapReduce implementation
# of an SQL relational join between tables line_item and order

import MapReduce
import sys

# Part 1: create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: emit word:document_id pairs avoiding duplicates
def mapper(record):
    # key: table identifier (line_item/order), not explicitly used
    # order_id: record id (for matching)
    order_id = record[1]
    mr.emit_intermediate(order_id, record)

# Part 3: remove duplicates from list_of_ids and emit it
def reducer(order_id, record_list):
    # order_id: record id
    # value: list of records (lists)

    # find the order entry and remove it from the list
    for record in record_list:
        if record[0] == "order":
            order_record = record
            break
    record_list.remove(order_record)

    # emit order_record + other record for each record remaining
    for record in record_list:
        mr.emit(order_record + record)

# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)
