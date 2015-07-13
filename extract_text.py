import os
import requests
import json
import sys

# Get the text from each tweet in a file and output it to the text collection file
def get_text(file_name, new_file):
    
    jsonFile=open(file_name, 'r')
    data = json.load(jsonFile)
    jsonFile.close()
    texts = []
    
    for tweet in data:
        texts.append(tweet[u'text'].encode('utf8'))

    # Write the text to the main text page for that hashtag quesry
    jsonFile = open(new_file, "w+")
    jsonFile.write(json.dumps(texts))
    jsonFile.close()

output_file = sys.argv[2]+ "/"
input_file = sys.argv[1] + "/"
# Create a new dir to collect all files of tweet text only with a given hashtag
output_dir = output_file
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

hashtag_folder = input_file
for dir in os.listdir(hashtag_folder):
    #print "in directory" + dir
    if dir.endswith("2015"):
        print "in directory" + dir
        for file in os.listdir(hashtag_folder + dir):
            if file.endswith(".json"):
                output_path = output_dir + "/" + file
                #get tweet texts from each file
                get_text(hashtag_folder + dir+"/"+ file, output_path)

