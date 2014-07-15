import sys
import json
import string  ## for list of letters

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    # read the file with scores into a dictionary
    scores = {}  ## initialize empty dictionary
    for line in sent_file:
        term, score = line.split("\t")  ## parse TAB-delimited file
        scores[term] = int(score)  ## add key-value pair
    
    # get sub-dictionary of phrases (keys with a space)
    phrase_scores = {key:score for key, score in scores.items() if key.find(" ") != -1}
    
    # parse the tweet file line by line
    for line in tweet_file:
        tweet = json.loads(line)  ## parse JSON text line
        # get tweet text (or return "" if no text field exists)
        tweet_text = tweet["text"] if "text" in tweet else ""
        # only keep letters and the space character
        tweet_text = "".join([c for c in tweet_text if c in string.letters or c == " "])
        
        # change everything to lowercase
        tweet_text = tweet_text.lower()
        
        tweet_words = tweet_text.split(" ")  ## get list of words
        # strip punctuation from words
        
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
