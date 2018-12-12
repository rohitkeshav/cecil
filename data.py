from bs4 import BeautifulSoup

import requests


BASE_URL = "https://www.indeed.com/jobs"
# Sample usage - "https://www.indeed.com/jobs?q=python+software+engineer+$135,000&l=new+york&jt=fulltime&explvl=entry_level"


def convert_2_qparams(rdict):

    retval = BASE_URL + '?'

    for k, v in rdict.items():
        retval += f'{k}={v}&'

    return retval


def scrape(soup):

    retval = {}

    for item in soup.find_all('div', {'data-tn-component': 'organicJob'}):
        imp = item.find('h2')

        soup = boil_soup({}, f"https://www.indeed.com{imp.find('a')['href']}")

        retval[imp.find('a').text] = soup.find('div', {'class', 'jobsearch-JobComponent-description icl-u-xs-mt--md'}).text

    return retval


def boil_soup(query_param, link=None):

    qp = convert_2_qparams(query_param) if query_param else link
    page = requests.get(qp)

    if page.status_code != 200:
        return

    return BeautifulSoup(page.text, features='lxml')


def get_jobs(query_param):

    soup = boil_soup(query_param)

    pagination = soup.find('div', 'pagination')
    plen = len(pagination.find_all('a'))

    run_till = plen if plen <= 4 else 4

    for p_num in range(0, run_till+1):
        query_param['start'] = (p_num + 1) * 10

        soup = boil_soup(query_param)

        scrape(soup)
