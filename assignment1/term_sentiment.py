import sys
import json

def get_scored_terms(infile):
    ''' (file open for reading) -> dict of {str:int}
    Return dictionary from word list and associated
    sentiment score in infile.
    '''
    # read the file with scores into a dictionary
    scores = {}  ## initialize empty dictionary
    for line in infile:
        term, score = line.split("\t")  ## parse TAB-delimited file
        scores[term] = int(score)  ## add key-value pair
    
    return scores


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



def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    # read the file with scores into a dictionary
    score = get_scored_terms(sent_file)
    
    # initialize dictionaries for positive and negative word counts
    positive = {}
    negative = {}
    
    # parse the tweet file line by line
    # and build positive and negative word counts
    for line in tweet_file:
        tweet = json.loads(line)  ## parse JSON text line
        # get tweet text (or return "" if no text field exists)
        tweet_text = tweet["text"] if "text" in tweet else ""
        tweet_text = clean_text(tweet_text)
        
        # get list of words from tweet text
        tweet_words = tweet_text.split(" ")
        
        # pass over words once to determine count
        # of positive and negative words
        pos_count = 0
        neg_count = 0
        for word in tweet_words:
            if word in score:
                if score[word] > 0:
                    pos_count += 1
                else:
                    neg_count += 1
                    
        # pass over words again adding counts to
        # each tally
        for word in tweet_words:
            if word not in score and len(word) > 2:
                if word in positive:
                    positive[word] += pos_count
                    negative[word] += neg_count
                else:
                    positive[word] = pos_count
                    negative[word] = neg_count
    
    # loop over dictionaries to print sentiment scores
    for word in positive:
        positive_hits = positive[word]
        # change negative_hits to 1 to avoid if it's 0
        # to avoid division by zero error
        negative_hits = negative[word] if negative[word] > 0 else 1 
        print word, float(positive_hits)/negative_hits

            
if __name__ == '__main__':
    main()
