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


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    scores = get_scored_terms(sent_file)
 
    # get sub-dictionary of phrases (keys with a space)
    phrase_scores = {key:score for key, score in scores.items() if key.find(" ") != -1}
    
    # parse the tweet file line by line
    for line in tweet_file:
        tweet = json.loads(line)  ## parse JSON text line
        # get tweet text (or return "" if no text field exists)
        tweet_text = tweet["text"] if "text" in tweet else ""
        tweet_text = clean_text(tweet_text)
        
        # get list of words from tweet text
        tweet_words = tweet_text.split(" ")
                
        # get sum of word scores
        sent_score = 0
        for word in tweet_words:
            if word in scores:
                sent_score += scores[word]
        
        # add sum of phrase scores (not essential, but cool)
        for phrase in phrase_scores.keys():
            if tweet_text.find(phrase) != -1:
                sent_score += phrase_scores[phrase]
        

        print sent_score
        
    
if __name__ == '__main__':
    main()
