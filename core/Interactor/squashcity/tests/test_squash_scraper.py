'''
Created on 3 Dec 2015

@author: ggiscan
'''
import unittest
import datetime as dt
from squashcity.squash_scraper import parse_page, read_static_schedule

class Test(unittest.TestCase):
    def testScraper(self):
        result = parse_page(read_static_schedule('res/squash.html'))
        test = [(sr.court, sr.start_date, sr.end_date) for sr in result if sr.court == 1]
        self.assertEqual(10, len(test))
        test = [sr.start_date for sr in result if sr.start_date == dt.datetime(2015,11,25, 7, 15)]
        self.assertEqual(4, len(test)) 
        test = [sr.start_date for sr in result if sr.start_date == dt.datetime(2015,11,25, 7, 30)]
        self.assertEqual(3, len(test)) 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()