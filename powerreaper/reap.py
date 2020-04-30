import requests
from bs4 import BeautifulSoup


def main():
    rows = scrape_data_rows()
    data = get_row_data(rows)
    print_data(data)


class power_data:
    def __init__(self, cols):
        self.division = cols[0]
        self.sub_division = cols[1]
        self.sub_station = cols[2]
        self.from_time = cols[3]
        self.to_time = cols[4]
        self.areas = cols[5]


def scrape_data_rows():
    URL = 'https://www.bescom.org/upo/public.php'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.find_all('tr')
    return rows


def get_row_data(rows):
    maxIndex = 11
    excludedIndices = [0, 1, 7, 8, 10, 11]
    data = []
    for row in rows:
        if None in row:
            continue
        cols = row.find_all('td')
        colData = []
        for index, val in enumerate(cols):
            if None in val:
                colData.append('N/A')
            if (not index in excludedIndices):
                colData.append(val.text.strip())
            if(index == maxIndex):
                data.append(power_data(colData))
    return data


def print_data(data):
    for datum in data:
        print(datum.division, datum.sub_division, datum.sub_station,
              datum.from_time, datum.to_time, datum.areas, sep=" --***-- ")
