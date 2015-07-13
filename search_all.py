import sys
import tweepy
import datetime
import urllib
import signal
import json
import pprint
import partitions
import datetime
import os

# This program gets all the tweet using tweepy Cursor. The search parameters are specified and we are chunking
# the tweets by day. Each file contains a max of 100 tweets and the max number of tweets/day is 80K
# Don't forget to install tweepy
# pip install tweepy

consumer_key = "";
consumer_secret = "";

access_token = "";
access_token_secret = "";

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Add retry arguments when rate limit has been reached
api = tweepy.API(auth_handler=auth,retry_count=3,retry_delay=5,retry_errors=set([401, 404, 500, 503]),wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
query = sys.argv[1]
q2 = urllib.quote_plus(query)  # URL encoded query, Arg 1
pp = pprint.PrettyPrinter()

xsdDatetimeFormat = "%Y-%m-%dT%H:%M:%S"
xsdDateFormat = "%Y-%m-%d"


start = datetime.datetime.strptime(sys.argv[2],xsdDateFormat) # start date, Arg 2
end = datetime.datetime.strptime(sys.argv[3],xsdDateFormat)   # end date, doesn't include, Arg 3

# Partition the dates by each day and store in array dates
dates = []
for d in partitions.date_partition(start,end):
    dates.append(d)

class TweetSerializer:
    
   out = None
   first = True
   count = 0
   
   #Create a file
   def start(self,q,file_no,day):
      self.count += 1
      #Create a directory for each hashtag and each date
      #Folder structure is .../hashtag/date/
      mypath = os.path.join(str(q),str(day))
      if not os.path.isdir(mypath):
        os.makedirs(mypath)
      fname = mypath + "/tweets-"+str(q)+" - "+str(file_no) +" - "+str(day)+".json"
      self.out = open(fname,"w")
      self.out.write("[\n")
      self.first = True
   
   #Close a file
   def end(self):
      if self.out is not None:
         self.out.write("\n]\n")
         self.out.close()
      self.out = None

   def write(self,tweet):
      if not self.first:  # if not first tweet, then add a comma and new line
         self.out.write(",\n")
      self.first = False # after start and after the first write, turn first to False
      #fields = self.create(params, tweet)
      jobj = json.dumps(tweet._json).encode('utf8')
      self.out.write(jobj)

   def create(self,fields, tweet):
       fieldlist= {} #create a dictionary with the param: tweet value of that param
       for item in fields:
           fieldlist[item] = tweet._json[item]
       return fieldlist
                         
serializer = TweetSerializer()

#KeyBoard Interrupt triggers this call:
def interrupt(signum, frame):
    print "Interruption... Closing"
    #make sure there is a closing ]
    serializer.end()
    exit(1)
signal.signal(signal.SIGINT, interrupt)



for i,d in enumerate(dates):
    day1= dates[i].date()
    if(dates[i]== (end - datetime.timedelta(days=1))):
        day2= dates[i] + datetime.timedelta(days=1)
    
    else:
        day2 = dates[i+1]
    day2 = day2.date()

    files_per_day_count = 1
    tweet_count = 0
    serializer.start(query,files_per_day_count,day1.strftime("%B %d, %Y")) # create a file
    closed_file = 0 # set flag that file is not closed

    # Collect all the tweets per a day , max is 8000 tweets/day, count is number of tweets per request
    # Just add them after the 'q' variable:" since= 2014-01-01 until= 2014-01-02"

    tw = tweepy.Cursor(api.search,q=q2,since= day1, until= day2, count=100).items(8000)
        
    while True:
            
            try:
                tweet = tw.next()
            
                # if file is closed and there are more tweets to process: start a new file and closed file to false
                if(closed_file == 1):
                    files_per_day_count = files_per_day_count + 1
                    serializer.start(query,files_per_day_count,day1.strftime("%B %d, %Y"))
                    closed_file = 0
                
                tweet_count = tweet_count + 1
                serializer.write(tweet)
                
                # store only 100 items per json file
                if(tweet_count > 99):
                    print "over 100 tweets\n"
                    # close the old file, reset tweet count , flag closed file to 1 (true)
                    closed_file = 1
                    tweet_count = 0
                    serializer.end()

            except tweepy.TweepError as e:
                    #if file is not closed, close the file
                    if(closed_file == 0):
                        serializer.end()
                        closed_file = 1
                    print "Error with Tweepy!!!" + str(e) +"\n"
                    continue

            except StopIteration:
                    print "No more Tweets for that day!!!\n"
                    #if file is not closed, close the file
                    if(closed_file == 0):
                        serializer.end()
                        closed_file = 1
                    #if there are no more items to be processed, then break from iteration and get next day's tweets
                    break











