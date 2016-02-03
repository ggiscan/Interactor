from collections import namedtuple
import datetime as dt
#from sendmail import sendmail
import requests
from bs4 import BeautifulSoup

search_result_type = namedtuple("search_result_type","court start_date end_date")

def free_court_dates(start_date, start_time):
    datetime = '{} {}'.format(start_date.split()[1], start_time)
    start_date = dt.datetime.strptime(datetime, '%d-%m-%Y %H:%M')
    return (start_date, start_date + dt.timedelta(minutes=45))

def parse_page(data):
    soup = BeautifulSoup(data)
    page_date = soup.find(id='matrix_date_title').string
    bs_free_courts = soup.find_all('td', type='free')
    result = []
    for bs_court in bs_free_courts:
        start_time, end_time =  free_court_dates(page_date, bs_court.span.string)
        court = search_result_type(int(bs_court['slot'])-50, start_time, end_time)
        result.append(court)
    return result
    
def readschedule():
    url = "http://squashcity.baanreserveren.nl/auth/login"
    details = {'username': 'ggiscan14', 'password' : 'squashcity'}
    r = requests.post(url, details)
    #print(r.content.decode('utf-8'))
    return r.content.decode('utf-8')

def read_static_schedule(fname):
    return open(fname).read()

if __name__ == '__main__':
    result = parse_page(read_static_schedule('squash.html'))
    result = [sr.start_date for sr in result if sr.court == 1]
    print result
    #if result:
    #    sendmail('Free court scan result', message.format(list=result))
