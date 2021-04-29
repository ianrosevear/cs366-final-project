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

    # increment api calls
    api_calls = n+1

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
