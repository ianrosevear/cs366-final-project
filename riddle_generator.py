#every 3 tries, wait 1 minute before generating more riddles (if everything fails, each p1, p2 try at generating riddles will take 18 calls).
import time
#use time.sleep(60) to wait 60 seconds before next execution
import requests
import csv
import riddle_functions as rf
import random

#randomly pick 30 words from the startword file "nouns.txt"
##with open("nouns.txt") as f, open("train_set.txt", "w") as train \
##     , open("test_set.txt", "w") as test:
##    nouns_list = []
##    for line in f:
##        line = line.strip("\n\"\,")
##        nouns_list.append(line)
##    random.shuffle(nouns_list)
##    train_set = nouns_list[:800]
##    test_set = nouns_list[800:]
##    for word in train_set:
##        train.write(word +"\n")
##    for word in test_set:
##        test.write(word + "\n")
startword_list=["dog", "horse", "house"]
def generate_riddles(startword, assertions):
    list_of_categories_p1 = ["D", "L", "U", "C", "I","H", "R"]
    list_of_categories_p2 = ["C", "H", "L", "P","U", "I", "R"]
    max_tries = 30
    i = 0
    j = 0
    candidate_riddles=[]
    print("generating a riddle for the startword", startword, "...")
    for n in range(max_tries):
##        if n % 3 == 2:
##            print("waiting 60 seconds")
        p1 = list_of_categories_p1[i]
        p2 = list_of_categories_p2[j]
        riddle_output = rf.find_pair(startword, p1, p2, assertions)
        if riddle_output == "Try new p1" or riddle_output == None:
            #print("e1")
            if n==max_tries:
                return "Sorry, we can't make a very good riddle with this startword."
            i = (i+1)%7
            continue
        if riddle_output == "Try new p2":
            #print("e2")
            if n==max_tries:
                return "Sorry, we can't make a very good riddle with this startword."
            j = (j+1)%7
            continue
        if riddle_output == "Try new p1 or p2":
            if n==max_tries:
                return "Sorry, we can't make a very good riddle with this startword."
            if n % 2 == 0:
                i = (i+1)%7
            else:
                j = (j+1)%7
            continue
        #print("e4")
        #print(riddle_output)
        candidate_riddles.append(rf.print_riddles(riddle_output[0],riddle_output[1],riddle_output[2],riddle_output[3],riddle_output[4]))
        if len(candidate_riddles) == 10:
            return candidate_riddles
        else:
            if n % 2 == 0:
                i = (i+1)%7
            else:
                j = (j+1)%7
            continue
        #return rf.print_riddles(riddle_output[0],riddle_output[1],riddle_output[2],riddle_output[3],riddle_output[4])
    return "Sorry, we can't make a very good riddle with this startword."

t = time.localtime()
current_time = time.strftime("%H:%M:%S",t)
filename = "riddle_output_"+current_time+".txt"
with open("assertions_list.csv") as fa, open(filename, "w") as out:
    reader = csv.reader(fa, delimiter="\t")
    assertions = list(reader)
    for word in startword_list:
        riddle = generate_riddles(word, assertions)
        print(riddle)
        print()
        out.write(str(riddle)+"\n")
