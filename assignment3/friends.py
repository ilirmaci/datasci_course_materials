# This script is a simple MapReduce implementation
# of counting the number of friends for each user in
# a social network

import MapReduce
import sys

# Part 1: create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: emit person:friend pairs
def mapper(friendship):
    # friendship: a list [personA, personB] indicating B is a friend of A
    mr.emit_intermediate(friendship[0], friendship[1])

# Part 3: count friends of each person
def reducer(person, friend_list):
    # person: user name whose friends we want to count
    # friend_list: list of friend names
    mr.emit((person, len(friend_list)))

# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)
