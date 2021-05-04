## https://github.com/commonsense/conceptnet5/wiki/API
## Note that we are limited to 1 API lookup per second
## or 60 per minute

## the requests package is used to make api requests
import requests
import riddle_functions as rf

# api calls total
ac = 0

def print_riddles(has, used, answer):
    return "What has "+ str(has)+\
    " but isn't used for " + str(used['edges'][0]['end']['@id'])+\
     "?\n"+ str(answer) +"!"

#idea for improving this function to work with more riddle types:
#def print_riddles(node2, node3, node1, code1, code2):
    #add another two input variables: code1 and code2 for the corresponding category types:
	#H: has a
	#C: capable of
	#U: used for
	#L: located at
	#D: desires
	#P: part of
    #output_string = ""
    #if code1 == H:
        #output_string += "What has" + str(node2)
    #if code1 == C:
        #output_string += "What can" + str(node2)
    #if code1 == U:
	#output_string += "What is used for" + str(node2)
    #if code1 == L:
	#output_string += "What is found at" + str(node2)
    #if code1 == D:
	#output_string += "What likes" + str(node2)
    #if code1 == P:
	#output_string += "What is part of" + str(node2)
    #if code2 == H:
	#output_string += "but doesn't have" + str(node3) + "?"
    #if code2 == C:
        #output_string += "but can't" + str(node3) + "?"
    #if code2 == U:
	#output_string += "but isn't used for" + str(node3) + "?"
    #if code2 == L:
	#output_string += "but isn't found at" + str(node3) + "?"
    #if code2 == D:
	#output_string += "but doesn't like" + str(node3) + "?"
    #if code2 == P:
	#output_string += "but isn't part of" + str(node3) + "?"
    #output_string += str(node1) + "!"
    #return output_string


## hardcode a start word for test purposes
startword = "dog"

## request form is 'http://api.conceptnet.io/c/en/' + word
## the form of an @id is /c/en/word
ac, node1 = rf.call_api(ac, "w", startword)

#node1_id = node1["@id"]
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





#if part of -> used case:
def find_pair_has(node1, index):
    global ac
    #checking index so that it doesn't loop forever on words that will not work in this form
    node1_id = node1["@id"]
    while index < 3:
        # query for things that node1 has
        ac, node1_has = rf.call_api(ac, "q", "start="+node1_id, "rel=/r/HasA")

        # try except block with recursion: tries the whole process on the first edge for node1_has,
        # and if this gives an exception in the end, tries again with index 2. Up to 5.
        try:
            # next we get the id of something that node1 has
            node2_hasid = node1_has['edges'][index]['end']['@id']

            # then we query for things that also have node2
            ac, has_node2 = rf.call_api(ac, "q", "end="+node2_hasid, "rel=/r/HasA")

            # next we get the id of something that has node2
            # and is dissimilar to node1
            # we can't do this too many times lest we overstep the limits
            # of the API. /relatedness counts as two requests
            max_similarity = .5 #idk what number to make this yet
            min_similarity = .05
            max_lookups = 5 #to make sure we don't try too many times
            node3_id = ""
            for n in has_node2['edges'][0:max_lookups]:
                curr_id = n['start']['@id']

                ac, relatedness = rf.call_api(ac, "r", "node1="+node1_id, "node2="+curr_id)

                if min_similarity < relatedness < max_similarity:
                    node3_id = curr_id
                    break

            ac, node3_used = rf.call_api(ac, "q", "start="+node3_id, "rel=/r/UsedFor")
            #for my proposed print function this would need to be added here instead
	    #of the current way of doing all of this in the printing stage:
            #node3_output = node3_used['edges'][0]['end']['@id']
            #output_string = print_riddles(node2_hasid, node3_output, node1_id)
            #maybe put this in a if else block that is inside a try except block to look
            #through the first 2 entries or something before going back and trying a
            #different original word
            output_string = print_riddles(node2_hasid, node3_used, node1_id)
        #if there is an error, try again with index 1 higher
        except:
            return find_pair_has(node1, index+1)
        #if there is no error, return the output string
        return output_string

print(find_pair_has(node1, 0))
print("\nAPI calls (counting relatedness as 2):", ac)
