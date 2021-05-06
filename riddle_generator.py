#every 3 tries, wait 1 minute before generating more riddles (if everything fails, each p1, p2 try at generating riddles will take 18 calls).
import time
#use time.sleep(60) to wait 60 seconds before next execution
import requests
import riddle_functions as rf
#todo: make a list of startwords
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

def generate_riddles(startword):
    list_of_categories_p1 = ["U", "L", "C", "L", "D", "P"]
    list_of_categories_p2 = ["C", "C", "H", "L", "D", "P"]
    max_tries = 9
    i = 0
    j = 0
    for n in range(max_tries):
        if n % 3 == 2:
            print("waiting 60 seconds")
            time.sleep(60)
        
        p1 = list_of_categories_p1[i]
        p2 = list_of_categories_p2[j]
        riddle_output = rf.find_pair(startword, p1, p2)
        if riddle_output == "Try new p1" or riddle_output == None:
            print("e1")
            if n==9:
                return "Sorry, no riddle can be made with this startword"
            i = i+1
            continue
        if riddle_output == "Try new p2":
            print("e2")
            if n==9:
                return "Sorry, no riddle can be made with this startword"
            j = j+1
            continue
        if riddle_output == "Try new p1 or p2":
            if n==9:
                return "Sorry, no riddle can be made with this startword"
            if n % 2 == 0:
                i = i+1
            else:
                j = j+1
            continue
        print("e4")
        print(riddle_output)
        return rf.print_riddles(riddle_output[0],riddle_output[1],riddle_output[2],riddle_output[3],riddle_output[4])
    return "Sorry, no riddle can be made with this startword"
        
for word in startword_list:
    print(generate_riddles(word))
    print("generating next riddle after 60 second cooldown...")
    print()
    time.sleep(60)
