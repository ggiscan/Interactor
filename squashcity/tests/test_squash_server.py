'''
Created on 3 Dec 2015

@author: ggiscan
'''
import unittest
import core.dbman as dbman
from core.tests.common import Message
from core.server import CommandServer
from core.commons import Context
from squashcity.squash_cmd import SquashCity
from squashcity.squash_scraper import search_result_type
from squashcity.squash_server import match

import datetime as dt

class TestSquashServer(unittest.TestCase):
    def setUp(self):
        self.messages = [('17 18', ('Luci', 2)),
                         ('11 18', ('Ina', 1)),
                         ('17 18', ('George', 0))]
        start_times = [dt.datetime.combine(dt.date.today(), dt.time(*h)) for h in
                       [(17, 0), (11, 0)]]
        self.search_results = [search_result_type(*l) for l in 
                               [(1, h, h + dt.timedelta(minutes=45)) for h in start_times]]
        self.session = dbman.new_session("memory")

    
    def test_squah_server(self):
        matches = self.create_and_test_matches()
        self.closing_test(matches)
        
    def create_and_test_matches(self):
        dbman.create_product("SquashCity", session=self.session)
        for m in self.messages:
            dbman.register_user("SquashCity", 
                                user_name=m[1][0], 
                                priority=m[1][1], 
                                session=self.session)
        server = CommandServer([Message(i, 'CMD SquashCity ' + msg[0], msg[1][0]) 
                                for (i,msg) in enumerate(self.messages)]) 
        #print list(server)
        context = Context(self.session)
        for c in list(server):
            _ = c.execute(context)
        requests = dbman.active_product_requests('squashcity', session=self.session)
        self.assertEqual(3, len(requests))

        matches = match(requests, self.search_results)
        req_george = dbman.active_user_requests('George', 'SquashCity', session=self.session)[0]
        self.assertEqual(self.search_results[0], matches[req_george])
        req_ina = dbman.active_user_requests('Ina', 'SquashCity', session=self.session)[0]
        self.assertEqual(self.search_results[1], matches[req_ina])
        req_lucian = dbman.active_user_requests('Luci', 'SquashCity', session=self.session)[0]
        self.assertFalse(req_lucian in matches)
        return matches
        
    def closing_test(self, matches):
        dbman.close_requests(matches, self.session)
        self.assertEqual(1, len(dbman.active_product_requests('squashcity', session=self.session)))
        self.assertEqual(1, len(dbman.active_user_requests('Luci', 'squashcity', session=self.session)))
        
        
        