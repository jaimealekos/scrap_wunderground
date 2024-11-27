# Returns a table with the columns 'Time', 'Precip. Rate' y 'Precip. Accum.'
# after extracting them from the daily data table of a given wunderground.com's weather station url
#
# today = scrap_wunderground("https://www.wunderground.com/dashboard/pws/ICHIVA39/table/2024-10-29/2024-10-29/daily")

import requests
from bs4 import BeautifulSoup

def scrap_wunderground(url):

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', class_='history-table')

    if len(tables) >= 2:
        table = tables[1]
        rows = []

        for tr in table.find_all('tr')[1:]:            
            td_elements = tr.find_all('td')

            if td_elements:
                row = [td.text.strip() for td in td_elements]
                rows.append(row)
