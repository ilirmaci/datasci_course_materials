# This script prints an unsorted list of
# terms and their relative frequencies in a 
# given file with tweets

import sys
import json


def clean_text(text):
    ''' (str) -> str
    Return text after keeping only letters and the
    space character.
    '''
    import string  ## for list of letters
    
    # split to characters and replace non-letter 
    # characters with space
    letter_list = [c if c in string.letters else " " for c in text]
    
    # join again into a string
    text = "".join(letter_list)
        
    # change everything to lowercase and return
    return text.lower()


def main():
    tweet_file = open(sys.argv[1])
    
    # initialize empty dictionary of word:occurrence
    occurrence = {}
    
    # parse the tweet file line by line
    for line in tweet_file:
        tweet = json.loads(line)  ## parse JSON text line
        # get tweet text (or return "" if no text field exists)
        tweet_text = tweet["text"] if "text" in tweet else ""
        tweet_text = clean_text(tweet_text)
        
        # get list of words from tweet text
        tweet_words = tweet_text.split(" ")
        
        for word in tweet_words:
            if word in occurrence:
                occurrence[word] += 1
            else:
                occurrence[word] = 1
        
    # remove "" from list
    blanks = occurrence.pop("", 0)
    
    # get sum of all terms
    total_occ = sum([occurrence[w] for w in occurrence])
    
    # print out all key:value pairs
    for word in occurrence:
        print word, float(occurrence[word])/total_occ

if __name__ == "__main__":
    main()
    
    
    
    
    
