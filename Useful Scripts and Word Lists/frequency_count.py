import requests
import time
import riddle_functions as rf

startword_list = ["water",
"time",
"way",
"year",
"work",
"government",
"day",
"man",
"world",
"life",
"part",
"house",
"course",
"case",
"system",
"place",
"end",
"group",
"company",
"party",
"information",
"school",
"fact",
"money",
"point",
"example",
"state",
"business",
"night",
"area",]


def CountFrequency(my_list):

    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1

    for key, value in freq.items():
        print ("%s : %d"%(key, value))


total_list =[]
ac = 0

for word in startword_list:
    time.sleep(2)
    id = "/c/en/" + word
    ac, edges = rf.call_api(ac, "q", "start="+id, "limit=1000")
    if len(edges) == 0:
        continue
    edges = edges['edges']

    for x in edges:
        total_list.append(x['rel']['label'])

CountFrequency(total_list)
