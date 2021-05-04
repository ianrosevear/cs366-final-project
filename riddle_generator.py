#every 3 tries, wait 1 minute before generating more riddles (if everything fails, each p1, p2 try at generating riddles will take 18 calls).
import time
#use time.sleep(60) to wait 60 seconds before next execution
import requests
import riddle_functions as rf
#todo: make a list of startwords
startword_list = ["dog", "bus", "shark", "pencil", "soup"]
def generate_riddles(startword):
    print("generating riddle for", startword, "...")
    riddle_output = rf.find_pair(startword, "H", "U")
    if riddle_output != None:
        return rf.print_riddles(riddle_output[0],riddle_output[1],riddle_output[2],riddle_output[3],riddle_output[4])
    riddle_output = rf.find_pair(startword, "H", "H")
    if riddle_output != None:
        return rf.print_riddles(riddle_output[0],riddle_output[1],riddle_output[2],riddle_output[3],riddle_output[4])
    riddle_output = rf.find_pair(startword, "C", "L")
    if riddle_output != None:
        return rf.print_riddles(riddle_output[0],riddle_output[1],riddle_output[2],riddle_output[3],riddle_output[4])
    print(" please wait... riddle generating in 60 seconds")
    time.sleep(60)
    riddle_output = rf.find_pair(startword, "L", "U")
    if riddle_output != None:
        return rf.print_riddles(riddle_output[0],riddle_output[1],riddle_output[2],riddle_output[3],riddle_output[4])
    riddle_output = rf.find_pair(startword, "U", "D")
    if riddle_output != None:
        return rf.print_riddles(riddle_output[0],riddle_output[1],riddle_output[2],riddle_output[3],riddle_output[4])
    riddle_output = rf.find_pair(startword, "P", "H")
    if riddle_output != None:
        return rf.print_riddles(riddle_output[0],riddle_output[1],riddle_output[2],riddle_output[3],riddle_output[4])
    print(" please wait... riddle generating in 60 seconds")
    time.sleep(60)
    #fill in other cases
    if riddle_output == None:
        return "Sorry, we can't make a riddle with this starting word"
for word in startword_list:
    print(generate_riddles(word))
    print("generating next riddle after 60 second cooldown...")
    print()
    time.sleep(60)
