# This script is a simple MapReduce implementation
# for multiplying two matrices in entry list (sparse) notation

import MapReduce
import sys

# Part 1: create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: emit entry value keyed using resulting entry index (row, column)
def mapper(entry):
    # entry: list of [matrix_id, row, colum, value]
    # matrix_id: str label a/b identifying first or second matrix
    # (row, col): row and column index of resulting matrix
    # order: order in which the current value will be matched
    # value: matrix entry value to be used in computation
    matrix_id = entry[0]
    value = entry[3]
    if matrix_id == "a":
        row = entry[1]
        order = entry[2]
        for col in range(5):
            mr.emit_intermediate((row, col), (order, value))
    else:
        col = entry[2]
        order = entry[1]
        for row in range(5):
            mr.emit_intermediate((row, col), (order, value))

# Part 3: remove duplicates and emit each sequence
def reducer(index, value_list):
    # index: index of resulting entry in matrix AxB
    # value_list: list of (order, value)
    
    # initiate empty list of calculation steps
    step_list = [[] for i in range(5)]
    
    # fill step list with entries from value_list
    for order, value in value_list:
        step_list[order].append(value)
    
    # go over each step of step_list and compute the product and sum them
    result = 0  ## initiate sum of products
    for step in step_list:
        if len(step) == 2:
            result += step[0] * step[1]
    if result != 0:   ## to preserve advantage of sparcity
        mr.emit((index[0], index[1], result))
        
# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)
