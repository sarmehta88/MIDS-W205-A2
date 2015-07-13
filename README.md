# MIDS-W205-A2
Assignment 2 Spring 2015 - twitter acquisition

Architecture Design:

1) In the command line, type python search_all.py hashtag query start-date end-date 
Example: python search_all.py “#Warriors”  2015-06-06 2015-06-12

The format for hashtag query is “#Warriors”, dates is “2015-06-06”
I ran this program to collect tweets from 2015-06-06 till 2015-06-12 by partitioning the tweets by day. Thus, the search_all.py calls partitions.py from within the program(thru an import statement) and first partitions the week(start date till end date) by each day. The MAX limit to collect tweets per each day is 80K and the max number of tweets per a file is 100.
The file created is now in the path ~/currentpath/#Warriors/June 6, 2015/tweets-#Warriors - 1 - June 06, 2015.json

2) Since I did not use a special twitter query to extract tweets with only hashtag but NOT the other (for example, #Warriors - #NBAFinals2015), I created a program called hash_remove.py which goes into each hashtag folder and removes tweets from each file that have the hashtag that I do not want to include. As a result, this does the same as the twitter call #Warriors NOT #NBAFinals2015. NOTE: for all folder names- Do not include the ending “/“
To run this program, type python hash_remove.py “path/to/hashtag/folder” “hashtag_term-to-remove” (Do not include the #)
Example: python hash_remove.py "/Users/sarumehta/desktop/#Warriors" "NBAFinals2015"


3) Next, I want to get only the text of the tweets from the raw data collected in the hashtag folders and create a corresponding folder that stores the text only.
Example: python extract_text.py “path/to/hashtag/folder”  “path/to/hashtag folder/text- #Warriors”

4)After extracting the texts from each of the collected tweets, I want to get the 30 most frequent words associated with each hashtag. After I traverse the folder where all the texts of the tweets of a specific hashtag are stored, I tokenize the text by white space and then remove stop words and punctuation from the text. For a list of stop words, I use the NLTK corpus library and for a list of punctuation, I use the string.punctuation library. If I am counting words associated with #Warriors, I also disregard words that have #warrior(s) since that is a duplicate of the hashtag word.(For time sake, I hardcoded this in and added it to the “ if not w.startswith(('\"', '\\','http','let','it’,’//‘,’warrior’)” line. Also, I made sure the text was first converted to lower case before excluding stop words,punctuation, and other special words like (rt, http(s), via). Next, I created a dictionary of words as the keys and their counts as the values. Then, I sorted the dictionary by the counts(values) in descending order and only output the first 30 words and their counts to a json file.

Example: python word_count.py “path/to/tweet-text/folder” “path/to/outputfile/wcount- #Warriors”

5) Lastly, I translated the word count file for each hashtag to a histogram(bar graph) that had the terms as the x-axis and the frequency as the y-axis. For this, I used Matplot.py 
Example: python histogram.py “path/to/word count” “hashtag” 

Brief Analysis:

Interestingly, the top frequent words associated with #NBAFinals2015 was game and lebron whereas the top frequent words associated with #Warriors was #nbafinals and game. Also, #cavs and game were the most frequent words tweeted along with both #Warriors and #NBAFinals2015. I noticed words related to the Warriors player Stephen Curry were included in tweets that had only the #Warriors but tweets searched with only #NBAFinals had more terms relating to the Cavaliers player Lebron James. Maybe, this suggests that more people were rooting for the Cavaliers than the Warriors. This correlation cannot, however, be substantiated solely by twitter data.

AWS S3 Bucket Links:

Here is the link to the public bucket, where I have 3 folders of the raw twitter data collected from each hashtag query

https://s3-us-west-1.amazonaws.com/saru-mehta-w205-spring-2015-assignment2/

To download a specific json file inside a hashtag folder use this link and replace the last part of url with the json file’s name:

https://s3-us-west-1.amazonaws.com/saru-mehta-w205-spring-2015-assignment2/%23Warriors+and+%23NBAFinals2015/tweets-%23Warriors+%23NBAFinals2015+-+1+-+June+07%2C+2015.json


Histogram Links:	
https://s3-us-west-1.amazonaws.com/saru-mehta-w205-spring-2015-assignment2/hist+-+%23NBAFinals2015.png

https://s3-us-west-1.amazonaws.com/saru-mehta-w205-spring-2015-assignment2/hist+-+%23Warriors.png

https://s3-us-west-1.amazonaws.com/saru-mehta-w205-spring-2015-assignment2/hist-+%23Warriors+and+%23NBAFinals2015.png

Word Count Analysis Links:

https://s3-us-west-1.amazonaws.com/saru-mehta-w205-spring-2015-assignment2/wcount+-+%23NBAFinals2015

https://s3-us-west-1.amazonaws.com/saru-mehta-w205-spring-2015-assignment2/wcount+-+%23Warriors

https://s3-us-west-1.amazonaws.com/saru-mehta-w205-spring-2015-assignment2/wcount+-+%23Warriors+%23NBAFinals2015
