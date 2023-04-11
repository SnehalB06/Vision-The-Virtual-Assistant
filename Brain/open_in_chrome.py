import os
import webbrowser
from time import sleep

open_keyword_list = ['open', 'visit', 'launch', 'start']
applications_list = ['google', 'facebook', 'instagram']

def replace_keyword(word, query):
    return query.replace(word, "")

response_success = "The command has been executed."
response_failure = "That dind't work. Please try again"

def run_command(Nameofweb):
    Link = f"https://www.{Nameofweb}.com"
    processed = webbrowser.open(Link)
    print(processed)

def processOpenQuery(Query):
    Query = str(Query).lower()

    if "visit" in Query:
        Nameofweb = replace_keyword('visit', Query).strip()
        run_command(Nameofweb)
        return response_success
    
    elif "open" in Query:
        Nameofweb = replace_keyword('open', Query).strip()
        run_command(Nameofweb)
        return response_success

    elif "launch" in Query:
        Nameofweb = replace_keyword('launch', Query).strip()
        run_command(Nameofweb)
        return response_success

    elif "start" in Query:
        Nameofweb= replace_keyword('launch', Query).strip()
        run_command(Nameofweb)
        return response_success
    
    else:
        return response_failure
