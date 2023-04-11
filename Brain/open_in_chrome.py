import os
import webbrowser
from time import sleep

open_keyword_list = ['open', 'visit', 'launch', 'start']
applications_list = ['google', 'facebook', 'instagram']

def replace_keyword(word, query):
    return query.replace(word, "")

response_success = "The Command has been executed."
response_failure = "That dind't work. Please try again"

def processOpenQuery(Query):
    Query = str(Query).lower()

    if "visit" in Query:
        Nameofweb = replace_keyword('visit', Query).strip()
        Link = f"https://www.{Nameofweb}.com"
        webbrowser.open(Link)
        return response_success
    
    elif "open" in Query:
        Nameofweb = replace_keyword('open', Query).strip()
        Link = f"https://www.{Nameofweb}.com"
        webbrowser.open(Link)
        return response_success

    elif "launch" in Query:
        Nameofweb = replace_keyword('launch', Query).strip()
        Link = f"https://www.{Nameofweb}.com"
        webbrowser.open(Link)
        return response_success

    elif "start" in Query:
        Nameoftheapp= replace_keyword('launch', Query).strip()
        if "chrome" in Nameoftheapp:
            os.open(r"/Applications/Google Chrome")
        return response_success
    
    else:
        return response_failure
