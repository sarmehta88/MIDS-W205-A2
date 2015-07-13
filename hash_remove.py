import os
import requests
import json
import sys

# Remove a specific tweet that contains a specific hashtag from each file in a folder
def remove_hashtags(file_name, remove):
    
    jsonFile=open(file_name, 'r+')
    data = json.load(jsonFile)
    jsonFile.close()
    
    for item in data:
        for ent in item[u'entities'][u'hashtags']:
            if ent[u'text'].lower() == remove.lower():
                #print "found nbafinals2015"
                print " fileName is " + str(file_name)
                data.remove(item)
                
                break

    jsonFile = open(file_name, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

folder = sys.argv[1] + "/"
remove = sys.argv[2]
hashtag_folder = folder 
for dir in os.listdir(hashtag_folder):
    #print "in directory" + dir
    if dir.endswith("2015"):
        print "in directory" + dir
        for file in os.listdir(hashtag_folder + dir):
            if file.endswith(".json"):
                #each file must be checked
                remove_hashtags(hashtag_folder + dir+"/"+ file, remove)

