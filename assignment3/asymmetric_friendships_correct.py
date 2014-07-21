# This script is a simple MapReduce implementation
# for listing all one-sided friendships

import MapReduce
import sys

# Part 1: create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: emit (personA, personB):personB that indicates B is a friend of A
def mapper(friendship):
    # friendship: list [personA, personB] showing B is a friend of A
    # key: (personA, personB) tuple indicating at connection between A and B
    key = tuple(sorted(friendship))
    mr.emit_intermediate(key, friendship[1])

# Part 3: emit friendship if both parties are not friends
def reducer(key, friend_list):
    # key: (personA, personB) tuple indicating at connection between A and B
    # friend_list: list of one or two entries indicating friended party(ies)
    # person: unrequited friend (A if only A is friend of B)
    # friend: non-reciprocating friend (B, if only A is friend of B)
    if len(friend_list) == 1:
        person = list(key)   ## start with both parties and remove friend
        friend = friend_list[0]
        person.remove(friend)
        mr.emit([person[0], friend])
        
# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)
