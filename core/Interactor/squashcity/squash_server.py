'''
Created on 26 Nov 2015

@author: ggiscan
'''
from time import sleep
from core.dbman import active_product_requests
from operator import attrgetter
import networkx as nx
from squash_scraper import readschedule, parse_page

def poll_requests(interval):
    while True:
        requests = active_product_requests("squash")
        search_results = parse_page(read_schedule())
        matches = match(requests, search_results)
        sleep(interval)

def match(requests, search_results):
    requests = sorted(requests, key=attrgetter('priority'))
    search_results = list(search_results)
    G = nx.Graph()
    for req in requests:
        for sr in search_results:
            if (sr.start_date,sr.end_date) in req:
                G.add_edge(req, sr, weight=100-req.priority)
    matches = nx.algorithms.matching.max_weight_matching(G, maxcardinality=True)
    return dict((k, matches[k]) for k in requests if k in matches)

def close_requests(fulfilled_requests, session):
    for (req, sr) in fulfilled_requests:
        req.close(sr.court, sr.start_date)
        
if __name__ == '__main__':
    pass