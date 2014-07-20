# This script prints a list of the top 10
# hashtags and the number of their occurrences 
# from a given file with tweets

import sys
import json
from operator import itemgetter


def main():
    tweet_file = open(sys.argv[1])
    
    # initialize empty dictionary of word:occurrence
    occurrence = {}
    
    # parse the tweet file line by line
    for line in tweet_file:
        tweet = json.loads(line)  ## parse JSON text line
        
        if "entities" in tweet:
            for tag in tweet["entities"]["hashtags"]:
                tag_text = tag["text"]
                if tag_text in occurrence:
                    occurrence[tag_text] += 1
                else:
                    occurrence[tag_text] = 1
    
    # get the 10ths largest number of occurrences
    occ_tuples = occurrence.items()
    occ_tuples.sort(key=itemgetter(1), reverse=True)
    
    for i in range(10):
        print occ_tuples[i][0], occ_tuples[i][1]

if __name__ == "__main__":
    main()
    
