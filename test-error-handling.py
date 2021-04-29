## https://github.com/commonsense/conceptnet5/wiki/API
## Note that we are limited to 1 API lookup per second
## or 60 per minute

## the requests package is used to make api requests
import requests
api_calls = 0

def call_api(s):
    global api_calls
    api_calls = api_calls + 1
    return requests.get(s).json()

def print_riddles(has, used, answer):
    return "What has"+ str(has)+ "but isn't used for" + str(used['edges'][0]['end']['@id'])+ "??"+ str(answer)
## hardcode a start word for test purposes
startword = "dog"

## form is 'http://api.conceptnet.io/c/en/' + word
api = "http://api.conceptnet.io"
node1 = call_api(api + "/c/en/" + startword)
node1_id = node1["@id"]
#if part of -> used case: 
def find_pair_has(node1, index):
    #checking index so that it doesn't loop forever on words that will not work in this form
    while index < 5:
        query = "/query?" +\
                "start=" + node1_id +\
                "&" +\
                "rel=/r/HasA"
        node1_has = call_api(api + query)
        # try except block with recursion: tries the whole process on the first edge for node1_has,
        # and if this gives an exception in the end, tries again with index 2. Up to 5.
        try:
            # next we get the id of something that node1 has
            node2_hasid = node1_has['edges'][index]['end']['@id']
            # then we query for things that also have node2
            query = "/query?" +\
                    "end=" + node2_partofid +\
                    "&" +\
                    "rel=/r/HasA"
            has_node2 = call_api(api + query)
            # next we get the id of something that has node2
            # and is dissimilar to node1
            # we can't do this too many times lest we overstep the limits
            # of the API. /relatedness counts as two requests
            max_similarity = .5 #idk what number to make this yet
            min_similarity = .05
            max_lookups = 5 #to make sure we don't try too many times
            node3_id = ""
            for i, n in enumerate(has_node2['edges'][0:max_lookups]):
                curr_id = n['start']['@id']
                related_lookup = "/relatedness?" +\
                                 "node1=" + node1_id +\
                                 "&" +\
                                 "node2=" + curr_id
                relatedness = call_api(api + related_lookup)['value']
                if min_similarity < relatedness < max_similarity:
                    node3_id = curr_id
                    break
            query = "/query?" +\
                    "start=" + node3_id +\
                    "&" +\
                    "rel=/r/UsedFor"
            node3_used = call_api(api + query)
            output_string = print_riddles(node2_hasid, node3_used, node1_id)
        #if there is an error, try again with index 1 higher
        except: 
            return find_pair_has(node1, index+1)
        #if there is no error, return the output string
        else:
            return output_string

        
#returns none for some reason?? can't figure out why
print(find_pair_has(node1, 0))
print(api_calls)


