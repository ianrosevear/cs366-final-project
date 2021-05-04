import requests

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
def find_pair(startword, p1, p2):

    global ac
    n1_id = "/c/en/"+startword

    if p1 == "H":
        rel1 = "rel=/r/HasA"
    #fill in other cases later
    if p2 == "U":
        rel2 = "rel=/r/UsedFor"
    #fill in other cases later


    #every edge starting from n1 that has p1
    ac, n1_p1 = rf.call_api(ac, "q", "start="+n1_id, rel1)
    if len(n1_p1) == 0:
        return None

    #for every edge from n1 to n2 across p1
    for n1_p1_n2 in n1_p1['edges'][0:2]:

        #get id of n2
        n2_id = n1_p1_n2['end']["@id"]
        print("n2_id", n2_id)

        #get edges that end in node2 w rel1 and start from n3
        ac, p1_n2 = rf.call_api(ac, "q", rel1, "end="+n2_id)
        if len(p1_n2) == 0:
            return None

        #for every edge from n3 to n2 across p1
        for n3_p1_n2 in p1_n2['edges'][0:2]:
            n3_id = n3_p1_n2['start']['@id']
            print("n3 id", n3_id)

            #make sure n3 and n1 are different
            max_sim = .5
            min_sim = .05
            ac, n1_n3_rscore = rf.call_api(ac, "r", "node1="+n1_id, "node2="+n3_id)
            if not (min_sim < n1_n3_rscore < max_sim):
                continue

            #get edges that go from n3 to n4 across p2
            ac, n3_p2 = rf.call_api(ac, "q", rel2, "start="+n3_id)
            #if n3 doesn't have any nodes on the other end of p2, error
            if len(n3_p2) == 0:
                return None

            #pick an n4
            n4_id = n3_p2['edges'][0]['end']['@id']
            #return (n2_id, n4_id, n1_id, p1, p2)

        #if all this works, break
        #if we ever get an error, continue

    return None



############################################################################


def print_riddles(node2, node3, node1, code1, code2):
    #add another two input variables: code1 and code2 for the corresponding category types:
	#H: has a
	#C: capable of
	#U: used for
	#L: located at
	#D: desires
	#P: part of
    output_string = ""
    if code1 == H:
        output_string += "What has" + str(node2)
    if code1 == C:
        output_string += "What can" + str(node2)
    if code1 == U:
	output_string += "What is used for" + str(node2)
    if code1 == L:
	output_string += "What is found at" + str(node2)
    if code1 == D:
	output_string += "What likes" + str(node2)
    if code1 == P:
	output_string += "What is part of" + str(node2)
    if code2 == H:
	output_string += "but doesn't have" + str(node3) + "?"
    if code2 == C:
        output_string += "but can't" + str(node3) + "?"
    if code2 == U:
	output_string += "but isn't used for" + str(node3) + "?"
    if code2 == L:
	output_string += "but isn't found at" + str(node3) + "?"
    if code2 == D:
	output_string += "but doesn't like" + str(node3) + "?"
    if code2 == P:
	output_string += "but isn't part of" + str(node3) + "?"
    output_string += str(node1) + "!"
    return output_string
