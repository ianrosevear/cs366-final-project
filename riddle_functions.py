import requests
import sys
import time
import random

# call_api
# take in n, type, a1, a2, a3....
# n: a variable keeping track of the number of API calls
# type: the type of request
#     supported types: "w"=word, "q"=query, "r"=relatedness
# args: any number of arguments for the request, separated by commas
# output: (num_api_calls, results_of_request)
# example call:
# api_calls, node2 = call_api(api_calls, "query", "start="+node1_id, "rel=/r/HasA")
def call_api(n, type, *args):

    # is this a relatedness request
    is_relatedness = False

    #generate type string
    if type == "w":
        type = "/c/en/"
    elif type == "q":
        type = "/query?"
    elif type == "r":
        type = "/relatedness?"
        is_relatedness = True
    # TODO: error if not recognized type?

    # increment api calls
    if is_relatedness:
        api_calls = n+2
    else:
        api_calls = n+1

    # generate request string
    api = "http://api.conceptnet.io"
    request_string = api + type
    # add parameters to request string
    for w in args:
        request_string = request_string + w + "&"
    # remove trailing "&"
    request_string = request_string[:-1]

    # if a relatedness request, return the value
    if is_relatedness:
        return (api_calls, requests.get(request_string).json()['value'])
    else:
        return (api_calls, requests.get(request_string).json())



############################################################################

# p1 is true of both things
# p2 is true of node3 but not answer(node1)
ac = 0
def find_pair1(startword, p1, p2):

    global ac
    n1_id = "/c/en/"+startword

    if p1 == "H":
        rel1 = "rel=/r/HasA"
    if p1 == "C":
        rel1 = "rel=/r/CapableOf"
    if p1 == "U":
        rel1 = "rel=/r/UsedFor"
    if p1 == "L":
        rel1 = "rel=/r/AtLocation"
    if p1 == "D":
        rel1 = "rel=/r/Desires"
    if p1 == "P":
        rel1 = "rel=/r/PartOf"
    if p1 == "R":
        rel1 = "rel=/r/RelatedTo"
    if p1 == "I":
        rel1 = "rel=/r/IsA"
    if p2 == "H":
        rel2 = "rel=/r/HasA"
    if p2 == "C":
        rel2 = "rel=/r/CapableOf"
    if p2 == "U":
        rel2 = "rel=/r/UsedFor"
    if p2 == "L":
        rel2 = "rel=/r/AtLocation"
    if p2 == "D":
        rel2 = "rel=/r/Desires"
    if p2 == "P":
        rel2 = "rel=/r/PartOf"
    if p2 == "R":
        rel2 = "rel=/r/RelatedTo"
    if p2 == "I":
        rel2 = "rel=/r/IsA"


    #every edge starting from n1 that has p1
    ac, n1_p1 = call_api(ac, "q", "start="+n1_id, rel1)
    if len(n1_p1) == 0:
        return None

    #for every edge from n1 to n2 across p1
    for j,n1_p1_n2 in enumerate(n1_p1['edges'][0:2]):

        #get id of n2
        n2_id = n1_p1_n2['end']["@id"]

        #get edges that end in node2 w rel1 and start from n3
        ac, p1_n2 = call_api(ac, "q", rel1, "end="+n2_id)
        if len(p1_n2) == 0:
            if j == 1:
                return "Try new p1"
            else:
                continue

        #for every edge from n3 to n2 across p1
        for i,n3_p1_n2 in enumerate(p1_n2['edges'][0:2]):
            #print(i)
            n3_id = n3_p1_n2['start']['@id']

            #make sure n3 and n1 are different
            max_sim = .5
            min_sim = .05
            ac, n1_n3_rscore = call_api(ac, "r", "node1="+n1_id, "node2="+n3_id)
            if not (min_sim < n1_n3_rscore < max_sim):
                continue

            #get edges that go from n3 to n4 across p2
            ac, n3_p2 = call_api(ac, "q", rel2, "start="+n3_id)
            #if n3 doesn't have any nodes on the other end of p2, error
            if len(n3_p2['edges']) == 0:
                if i == 1:
                    return "Try new p2"
                else:
                    continue
           #pick an n4
            ac, n1_p2 = call_api(ac, "q", rel2, "start="+n1_id)
            n1_p2_list = []
            for x in range(len(n1_p2['edges'])):
                n1_p2_list.append(n1_p2['edges'][x]['end']['@id'])
            #n4_id = n3_p2['edges'][0]['end']['@id']
            for x in range(len(n3_p2['edges'])):
                n4_id = n3_p2['edges'][x]['end']['@id']
                if n4_id not in n1_p2_list:
                    return (n2_id, n4_id, n1_id, p1, p2)


        #if all this works, break
        #if we ever get an error, continue

    return "Try new p1 or p2"



def find_pair(startword, p1, p2, assertions):

    n1_id = "/c/en/"+startword+"/"

    if p1 == "H":
        rel1 = "/r/HasA/"
    if p1 == "C":
        rel1 = "/r/CapableOf/"
    if p1 == "U":
        rel1 = "/r/UsedFor/"
    if p1 == "L":
        rel1 = "/r/AtLocation/"
    if p1 == "D":
        rel1 = "/r/Desires/"
    if p1 == "P":
        rel1 = "/r/PartOf/"
    if p1 == "R":
        rel1 = "/r/RelatedTo/"
    if p1 == "I":
        rel1 = "/r/IsA/"
    if p2 == "H":
        rel2 = "/r/HasA/"
    if p2 == "C":
        rel2 = "/r/CapableOf/"
    if p2 == "U":
        rel2 = "/r/UsedFor/"
    if p2 == "L":
        rel2 = "/r/AtLocation/"
    if p2 == "D":
        rel2 = "/r/Desires/"
    if p2 == "P":
        rel2 = "/r/PartOf/"
    if p2 == "R":
        rel2 = "/r/RelatedTo/"
    if p2 == "I":
        rel2 = "/r/IsA/"


    #every edge starting from n1 that has p1
    n1_p1 = get_assertions_start(n1_id, rel1, assertions)
    if len(n1_p1) == 0:
        return None

    #for every edge from n1 to n2 across p1
    for j, n1_p1_n2 in enumerate(n1_p1[0:20]):

        #get id of n2
        n2_id = n1_p1_n2[2]
        #get edges that end in node2 w rel1 and start from n3
        p1_n2 = get_assertions_end(n2_id, rel1, assertions)
        #print("p1_n2", p1_n2)
        if len(p1_n2) == 0:
            if j == 1:
                return "Try new p1"
            else:
                continue

        #for every edge from n3 to n2 across p1
        for i,n3_p1_n2 in enumerate(p1_n2[0:20]):
            n3_id = n3_p1_n2[1]
            #get edges that go from n3 to n4 across p2
            n3_p2 = get_assertions_start(n3_id, rel2, assertions)
            #if n3 doesn't have any nodes on the other end of p2, error
            if len(n3_p2) == 0:
                if i == 1:
                    return "Try new p2"
                else:
                    continue
           #pick an n4
            n1_p2 = get_assertions_start(n1_id, rel2, assertions)
            n1_p2_list = [row[2] for row in n1_p2]
            n4_list=[]
            for row in n3_p2:
                n4_id = row[2]
                if n4_id not in n1_p2_list:
                    n4_list.append(n4_id)
            length = len(n4_list)
            if length != 0:
                index = random.randint(0, length-1)
                n4_chosen = n4_list[index]
                return (n2_id, n4_chosen, n1_id, p1, p2)
        #if all this works, break
        #if we ever get an error, continue

    return "Try new p1 or p2"

############################################################################
def clean(node):
    node = node.replace("_", " ")
    node = node.replace("/c/en/", "")
    return node
############################################################################
##def sleep(timer):
##    for i in range(0,timer):
##        time_left = timer-i
##        print(time_left, end = "", flush = True)
##        time.sleep(1)
############################################################################
def print_riddles(node2, node3, node1, code1, code2):
    #add another two input variables: code1 and code2 for the corresponding category types:
	#H: has a
	#C: capable of
	#U: used for
	#L: located at
	#D: desires
	#P: part of
    node2 = clean(node2)
    node3 = clean(node3)
    node1 = clean(node1)
    output_string = ""
    if code1 == "H":
        output_string += "What has " + str(node2)
    if code1 == "C":
        output_string += "What can " + str(node2)
    if code1 == "U":
        output_string += "What is used for " + str(node2)
    if code1 == "L":
        output_string += "What is found at " + str(node2)
    if code1 == "D":
        output_string += "What likes " + str(node2)
    if code1 == "P":
        output_string += "What is part of " + str(node2)
    if code1 == "R":
        output_string += "What is related to " + str(node2)
    if code1 =="I":
        output_string += "What is a " + str(node2)
    if code2 == "H":
        output_string += " but doesn't have " + str(node3) + "?"
    if code2 == "C":
        output_string += " but can't " + str(node3) + "?"
    if code2 == "U":
        output_string += " but isn't used for " + str(node3) + "?"
    if code2 == "L":
        output_string += " but isn't found at " + str(node3) + "?"
    if code2 == "D":
        output_string += " but doesn't like " + str(node3) + "?"
    if code2 == "P":
        output_string += " but isn't part of " + str(node3) + "?"
    if code2 == "R":
        output_string += " but isn't related to " + str(node3) + "?"
    if code2 == "I":
        output_string += " but is not a " + str(node3) + "?"
    output_string += " " + str(node1) + "!"
    return output_string
############################################################################

# start, rel --> list of edges
# start = /c/en/word
# rel = /r/HasA
def get_assertions_start(start, rel, assertions):

    output_list = []
    for line in assertions:
        if line[1] == start and line[0] == rel:
            output_list.append(line)

    return output_list
def get_assertions_end(end, rel, assertions):

    output_list = []
    for line in assertions:
        if line[2] == end and line[0] == rel:
            output_list.append(line)

    return output_list
##def get_assertions_end(end, rel, assertions):
##    output_list = []
##
##    for line in assertions:
##        print(line)
##        if line[2] == end and line[0] == rel:
##            output_list.append(line)
##        break
##
##    return output_list
