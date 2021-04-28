## https://github.com/commonsense/conceptnet5/wiki/API
## Note that we are limited to 1 API lookup per second
## or 60 per minute

## the requests package is used to make api requests
import requests
api_calls = 0

def call_api(s):
    api_calls += 1
    return requests.get(s).json()


## hardcode a start word for test purposes
startword = "table"

## form is 'http://api.conceptnet.io/c/en/' + word
api = "http://api.conceptnet.io"
node1 = call_api(api + "/c/en/" + startword)

## to find all the "HasA" edges that start from "table":
# first get the id of the node we are working with:
# this will look like /c/en/table
node1_id = node1["@id"]

# to get a list of all things the node1 has,
# we can do a query with the parameters:
# "/query?" --> signifies a query
# "start=" + node_id --> start the edge from 'node1_id' node
# "&" --> connect the parameters
# "rel=/r/HasA" --> edge has relation type "HasA"
query = "/query?" +\
        "start=" + node1_id +\
        "&" +\
        "rel=/r/HasA"
node1_has = call_api(api + query)

### doing this directly appears not to work for some reason
##relations = "http://api.conceptnet.io" +\
##            node1_id +\
##            "?rel=/r/HasA" +\
##            "&" +\
##            "limit=100"
##node1_has = requests.get(relations).json()

# next we get the id of something that node1 has
node2_id = node1_has['edges'][0]['end']['@id']

# then we query for things that also have node2
query = "/query?" +\
        "end=" + node2_id +\
        "&" +\
        "rel=/r/HasA"
has_node2 = call_api(api + query)

# next we get the id of something that has node2
# and is dissimilar to node1
# we can't do this too many times lest we overstep the limits
# of the API. /relatedness counts as two requests
max_similarity = 5 #idk what number to make this yet
max_lookups = 5 #to make sure we don't try too many times

node3_id = ""
for i, n in enumerate(has_node2['edges'][0:max_lookups]):
    curr_id = n['start']['@id']
    related_lookup = "/relatedness?" +\
                     "node1=" + node1_id +\
                     "&" +\
                     "node2=" + curr_id

    relatedness = call_api(api + related_lookup)['value']

    if relatedness < max_similarity:
        node3_id = curr_id
        break








print(api_calls)
