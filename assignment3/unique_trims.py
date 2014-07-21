# This script is a simple MapReduce implementation
# for returning all unique occurrences of trimmed
# DNA sequences

import MapReduce
import sys

# Part 1: create MapReduce object
mr = MapReduce.MapReduce()

# Part 2: emit trimmed sequences keyed by first few nucleotides
def mapper(key_sequence_pair):
    # key_sequence_pair: list of [seq_key, sequence]
    # sequence: DNA sequence to be trimmed
    # key: first 6 nucleotides of sequence, used as reducer key
    sequence = key_sequence_pair[1]
    key = sequence[0:6]
    mr.emit_intermediate(key, sequence[:-10])

# Part 3: remove duplicates and emit each sequence
def reducer(key, dna_list):
    # key: first 6 nucleotides of sequence
    # dna_list: list of trimmed DNA sequences starting with key
    dna_list = set(dna_list)  ## removes duplicates
    for sequence in dna_list:
        mr.emit(sequence)
        
        
# Part 4
inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)
