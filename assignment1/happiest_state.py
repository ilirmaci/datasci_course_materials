# This script determines the state with the highest average
# sentiment score of tweets originating from the state

import json
import sys
#from operator import getitem  ## needed for final tuple list sort

def coord_to_state(latlon):
    '''([float, float]) -> str or NoneType
    Return state abbreviation where latlon coordinates fall. If latlon does
    not fall in any state, return None.
    '''
    
    # disctionary of state bounding boxes
    bound_box={"AL":[-88.4761428833008,-84.9008865356445,30.2407131195068,35.0134506225586], 
           "AZ":[-114.809280395508,-109.039596557617,31.3465213775635,37.0016136169434], 
           "AK":[-94.6239776611328,-89.6507034301758,32.996639251709,36.5088691711426], 
           "CA":[-124.383415222168,-114.133193969727,32.538272857666,42.0207252502441],
           "CO":[-109.062515258789,-102.043785095215,36.9844245910645,41.0180473327637], 
           "CT":[-73.7224807739258,-71.7801513671875,41.0123176574707,42.049373626709],
           "DW":[-75.8023147583008,-75.0517425537109,38.4569244384766,39.8492164611816], 
           "DC":[-77.1373062133789,-76.9310455322266,38.8064308166504,38.9955062866211], 
           "FL":[-87.6396255493164,-80.0421981811523,25.1299285888672,31.0084743499756], 
           "GA":[-85.6113510131836,-80.8443450927734,30.3553047180176,34.996265411377], 
           "ID":[-117.232887268066,-111.050682067871,41.9978065490723,48.9936180114746], 
           "IL":[-91.5013580322266,-87.4963836669922,37.0016136169434,42.507740020752], 
           "IN":[-88.1037216186523,-84.7977523803711,37.7865676879883,41.7800827026367], 
           "IA":[-96.6064147949219,-90.1377182006836,40.376335144043,43.5104141235352], 
           "KS":[-102.060966491699,-94.583869934082,36.9958839416504,40.0210990905762], 
           "KY":[-89.4043350219727,-81.9673461914062,36.4974136352539,39.1330184936523], 
           "LA":[-94.056755065918,-89.0261840820312,28.9802055358887,33.0367469787598], 
           "ME":[-71.0754165649414,-67.0074157714844,43.0635108947754,47.4695510864258], 
           "MD":[-79.4978942871094,-75.0574645996094,37.9183502197266,39.7346229553223], 
           "MA":[-73.504753112793,-69.9466934204102,41.4993362426758,42.8744316101074], 
           "MA1":[-70.2102432250977,-69.9524230957031,41.2415008544922,41.3847427368164], 
           "MI":[-90.4127349853516,-83.90966796875,45.0975074768066,47.481014251709], 
           "MI1":[-86.8202972412109,-82.4428939819336,41.7113265991211,45.7907867431641], 
           "MN":[-97.225212097168,-89.4730911254883,43.4932289123535,49.3832321166992], 
           "MS":[-91.6331405639648,-88.1094436645508,30.1834144592285,34.996265411377], 
           "MO":[-95.76416015625,-89.0834808349609,35.9989395141602,40.6169776916504], 
           "MT":[-116.046867370605,-104.043403625488,44.3698501586914,49.0050811767578], 
           "NE":[-104.060592651367,-95.3344497680664,39.9981803894043,43.0062103271484], 
           "NV":[-120.006011962891,-114.035797119141,35.0191802978516,42.0092658996582], 
           "NH":[-72.5536422729492,-70.7316436767578,42.6968154907227,45.3152313232422], 
           "NJ":[-75.5502166748047,-73.9001007080078,38.9267539978027,41.3675537109375], 
           "NM":[-109.056785583496,-103.000625610352,31.3465213775635,37.0016136169434], 
           "NY":[-74.0261535644531,-73.9287414550781,40.7086524963379,40.8404350280762], 
           "NY1":[-79.7671813964844,-73.2583847045898,40.8060531616211,45.0115661621094], 
           "NY2":[-74.2954406738281,-74.0605239868164,40.4851989746094,40.6628150939941], 
           "NY3":[-74.0261535644531,-71.877555847168,40.548225402832,41.1555557250977], 
           "NC":[-75.8939895629883,-75.5387573242188,35.7926750183105,36.5547065734863], 
           "NC1":[-84.3221969604492,-75.7049179077148,33.8618049621582,36.5948143005371], 
           "NC2":[-76.0028533935547,-75.9111785888672,36.4916839599609,36.5547065734863], 
           "ND":[-104.049133300781,-96.5376586914062,45.934024810791,49.0050811767578], 
           "OH":[-84.820671081543,-80.5120315551758,38.428279876709,41.9691581726074], 
           "OK":[-103.00634765625,-94.4406356811523,33.6612701416016,37.0245323181152], 
           "OR":[-124.532379150391,-116.465133666992,42.0035362243652,46.2262344360352], 
           "PA":[-80.5349426269531,-74.7251586914062,39.7231636047363,42.2613677978516], 
           "RI":[-71.8603668212891,-71.1097869873047,41.3045272827148,42.0264549255371], 
           "SC":[-83.365364074707,-78.5582427978516,32.0397987365723,35.2082557678223], 
           "SD":[-104.066329956055,-96.4287948608398,42.4733619689941,45.9397583007812], 
           "TN":[-90.2866897583008,-81.646484375,34.9790725708008,36.6750297546387], 
           "TX":[-106.650367736816,-93.5353622436523,25.9377994537354,36.4916839599609], 
           "UT":[-114.047248840332,-109.039596557617,36.9958839416504,42.0035362243652], 
           "VT":[-73.4531860351562,-71.5051345825195,42.7311935424805,45.023021697998], 
           "VA":[-76.0143127441406,-75.3611373901367,37.1219329833984,38.0272064208984], 
           "VA1":[-75.3668670654297,-75.217903137207,37.8495941162109,38.0386695861816], 
           "VA2":[-83.646110534668,-75.8596115112305,36.5375213623047,39.4596061706543], 
           "WA":[-123.117164611816,-122.939552307129,48.4378509521484,48.6154708862305], 
           "WA1":[-122.887985229492,-122.756202697754,48.4034729003906,48.5409812927246], 
           "WA2":[-122.951011657715,-122.716094970703,48.5925521850586,48.7186012268066], 
           "WA3":[-122.721832275391,-122.309303283691,47.8992729187012,48.3748245239258], 
           "WA4":[-124.681343078613,-116.923492431641,45.532958984375,49.0050811767578], 
           "WV":[-82.6205139160156,-77.7159957885742,37.2021484375,40.6456260681152], 
           "WI":[-92.9222946166992,-86.9578018188477,42.496280670166,46.9367027282715], 
           "WY":[-111.062141418457,-104.054862976074,40.9893989562988,45.0058326721191]}
    
    # check if latlon falls into any bounding boxes, return if so 
    for state, box in bound_box.items():
        if box[0] < latlon[1] <  box[1] and box[2] < latlon[0] < box[3]:
            return(state[0:2])


def place_to_state(place):
    '''(str) -> str or NoneType
    Return US state if either its name or the capitalized abbreviation 
    appears in place. Otherwise return None.
    '''
    states = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 
          'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California',
          'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia',
          'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam',
          'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois',
          'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
          'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 
          'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri',
          'MP': 'Northern Mariana Islands', 'MS': 'Mississippi',
          'MT': 'Montana', 'NA': 'National', 'NC': 'North Carolina',
          'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire',
          'NJ': 'New Jersey', 'NM': 'New Mexico',
          'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma',
          'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 
          'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota',
          'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia',
          'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 
          'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'}
    
    for abb, state in states.items():
        if place.find(abb) != -1 or place.lower().find(state.lower()) != -1:
            return abb

def get_state(tweet):
    '''(tweet) -> str or NoneType
    Return US state abbreviation from where the tweet was sent. Return None
    if tweet cannot be placed in the US.
    '''
    if "geo" in tweet and tweet["geo"] != None:
        return coord_to_state(tweet["geo"]["coordinates"])
    if "place" in tweet and tweet["place"] != None:
        return place_to_state(tweet["place"]["full_name"])
    if tweet["user"]["location"] != []:
        return place_to_state(tweet["user"]["location"])


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
    
    # initialize dictionary of tweet sentiments by state:list of scores
    state_mood = {}
    
    # parse the tweet file line by line
    for line in tweet_file:
        tweet = json.loads(line)  ## parse JSON text line
        
        if "user" not in tweet:
            continue  ## skip if not a tweet
        
        # get tweet location
        state = get_state(tweet)       
        if state == None:
            continue  ## skip tweet if it's not placed in a US state
             
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
        
        # append to list of scores for that state
        if state in state_mood:
            state_mood[state].append(sent_score)
        else:
            state_mood[state] = [sent_score]
               
    mood_tuples = [(abb, float(sum(mood_list))/len(mood_list)) for 
                   abb, mood_list in state_mood.items()]            
    
    print max(mood_tuples, key=lambda x:x[1])[0]           
    
if __name__ == "__main__":
    main()