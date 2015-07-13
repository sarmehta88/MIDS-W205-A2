import string
import nltk
from nltk.corpus import stopwords
import os
import json
import simplejson
import sys

# Compare the count of word1 with word2, if the count is the same, perform cmp on the word strings
def compareItems((w1,c1), (w2,c2)):
    if c1 > c2:
        return - 1
    elif c1 == c2:
        return cmp(w1, w2)
    else:
        return 1

# Tokenize the tweet by white space but first replace some punctuations with white space
def tokenize_tweets(fname):
    #get the text from the file and covert to lower case
    text = open(fname,'r').read()
    text = string.lower(text)
    
    # replace punctuations with a space for easy tokenization
    
    for ch in '!"-?:':
        text = string.replace(text, ch, ' ')
    
    
    
    words = text.split()
    return words

# return the n high frequency words associated with a hashtag
def main():
    # n is the number of highest frequency words to get from this program
    n = 30
    output_file = sys.argv[2]
    # go to each folder and perform word_count on each file
    hashtag_folder = sys.argv[1]+ "/"
    counts = {}
    for file in os.listdir(hashtag_folder):
        if file.endswith(".json"):
            #each file must be checked
            words = tokenize_tweets(hashtag_folder + file)
            # create a list of stop words
            #stops = set(stopwords.words('english'))
            punctuation = list(string.punctuation)
            #exclude words that are trivial and punctuation
            stops = stopwords.words('english') + punctuation + ['rt', 'via', 'de', 'like','i\'m','&amp;','ko''l']
            #exclude_list = ['#nbafinal?.*','https?.*']

            # construct a dictionary of word counts
            for w in words:
                # add the hashtag to the list of words to exclude since we do not care of the count of original hashtag
                if w.lower() not in stops and not w.isdigit():
                    if not w.startswith(('\"', '\\','http','let','it','//')):
                        if not w.endswith(('.')):
                            #w.startswith('\"') and not w.startswith('\\'):
                            counts[w] = counts.get(w,0) + 1

    # output the n most frequent words.
    items = counts.items()
    items.sort(compareItems)
    
    jsonFile = open(output_file, "w+")
    dict = {}
    for i in range(n):
        dict[items[i][0]]= items[i][1]
    
    jsonFile.write(json.dumps(dict))
    jsonFile.close()

# call the main function
if __name__ == '__main__': main()