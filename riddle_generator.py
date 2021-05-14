#every 3 tries, wait 1 minute before generating more riddles (if everything fails, each p1, p2 try at generating riddles will take 18 calls).
import time
#use time.sleep(60) to wait 60 seconds before next execution
import requests
import csv
import riddle_functions as rf
import random

#randomly pick 30 words from the startword file "nouns.txt"
with open("nouns.txt") as f:
    nouns_list = []
    for line in f:
        line = line.strip("\n\"\,")
        nouns_list.append(line)
startword_list = random.sample(nouns_list, 30)
print(startword_list)
##startword_list = ["water","time",
##"way",
##"year",
##"work",
##"government",
##"day",
##"man",
##"world",
##"life",
##"part",
##"house",
##"course",
##"case",
##"system",
##"place",
##"end",
##"group",
##"company",
##"party",
##"information",
##"school",
##"fact",
##"money"]

def generate_riddles(startword, assertions):
    list_of_categories_p1 = ["D", "L", "U", "R", "C", "I"]
    list_of_categories_p2 = ["I", "C", "H", "L", "R", "P"]
    max_tries = 9
    i = 0
    j = 0
    print("generating a riddle for the startword", startword, "...")
    for n in range(max_tries):
##        if n % 3 == 2:
##            print("waiting 60 seconds")
        p1 = list_of_categories_p1[i]
        p2 = list_of_categories_p2[j]
        riddle_output = rf.find_pair(startword, p1, p2, assertions)
        if riddle_output == "Try new p1" or riddle_output == None:
            #print("e1")
            if n==9:
                return "Sorry, we can't make a very good riddle with this startword."
            i = (i+1)%6
            continue
        if riddle_output == "Try new p2":
            #print("e2")
            if n==9:
                return "Sorry, we can't make a very good riddle with this startword."
            j = (j+1)%6
            continue
        if riddle_output == "Try new p1 or p2":
            if n==9:
                return "Sorry, we can't make a very good riddle with this startword."
            if n % 2 == 0:
                i = (i+1)%6
            else:
                j = (j+1)%6
            continue
        #print("e4")
        #print(riddle_output)
        return rf.print_riddles(riddle_output[0],riddle_output[1],riddle_output[2],riddle_output[3],riddle_output[4])
    return "Sorry, we can't make a very good riddle with this startword."


with open("assertions_list.csv") as fa:
    reader = csv.reader(fa, delimiter="\t")
    assertions = list(reader)
    for word in startword_list:
        print(generate_riddles(word, assertions))
        print()
