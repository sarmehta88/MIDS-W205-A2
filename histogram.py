import numpy as np
import matplotlib.pyplot as plt
import json
import sys

def read_json_file(name):
    with open(name, "r") as f:
        return json.load(f)

#Open the word count file (json)
file_name = sys.argv[1]
d = read_json_file(file_name)

# Sort the data according to count in descending order
sorted_data = [ (count, word) for word, count in d.items() ]
sorted_data.sort(reverse= True)

hashtag = sys.argv[2]
# convert the tuple(count,word) to a list called words. words[0] is the counts words[1] is the terms
words = zip(*sorted_data)
# use numpy to create space for number of words(30)
pos = np.arange(len(words[1]))
width = 1.0

# Create a bar graph with where the words are the x axis, frequency is y axis
ax = plt.axes()
ax.set_xticks(pos + (width/2))
ax.set_xticklabels(words[1], rotation=90, ha='center')
plt.ylabel('Word Frequency')
plt.title('Top 30 Words asscociated with '+hashtag)
plt.bar(pos,words[0], width, color='r')

#plt.show()
graph_name = "graph- " + hashtag + ".png"
plt.savefig(graph_name)