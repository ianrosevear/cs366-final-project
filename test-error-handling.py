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



## hardcode a start word for test purposes
startword = "dog"

## request form is 'http://api.conceptnet.io/c/en/' + word
## the form of an @id is /c/en/word
ac, node1 = rf.call_api(ac, "w", startword)

#node1_id = node1["@id"]
#if part of -> used case:
def find_pair_has(node1, index):
    global ac
    #checking index so that it doesn't loop forever on words that will not work in this form
    node1_id = node1["@id"]
    while index < 5:
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

            output_string = print_riddles(node2_hasid, node3_used, node1_id)
        #if there is an error, try again with index 1 higher
        except:
            return find_pair_has(node1, index+1)
        #if there is no error, return the output string
        return output_string


#returns none for some reason?? can't figure out why
print(find_pair_has(node1, 0))
print("\nAPI calls (counting relatedness as 2):", ac)
