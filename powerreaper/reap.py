import click
import requests
from bs4 import BeautifulSoup


class term_colors:
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class power_data:
    def __init__(self, cols):
        self.division = cols[0]
        self.sub_division = cols[1]
        self.sub_station = cols[2]
        self.from_time = cols[3]
        self.to_time = cols[4]
        self.areas = cols[5]


def print_success(message):
    print(f"{term_colors.OK}{message}{term_colors.ENDC}")


def print_error(message):
    print(f"{term_colors.FAIL}{message}{term_colors.ENDC}")


def print_warning(message):
    print(f"{term_colors.WARNING}{message}{term_colors.ENDC}")


@click.command()
@click.option(
    "--debug", "is_debug", help="displays scrapped data on console instead of writing it to the file",
    flag_value=True,
    default=False
)
def main(is_debug):
    print_success("PowerReaper: Starting the scrapper...")
    rows = scrape_data_rows()
    data = []
    if None in rows:
        print_error("PowerReaper: The rows are empty! Aborting Scrapper!")
        return
    else:
        data = get_row_data(rows)
    if len(data) > 0:
        if is_debug:
            print_data(data)
        else:
            write_to_file(data)
            print_success("PowerReaper: Scrapper run completed")
    else:
        print_error("PowerReaper: No Data! Aborting Scrapper!")
        return


def scrape_data_rows():
    print_success("PowerReaper: initiating request to the web page...")
    try:
        URL = 'https://www.bescom.org/upo/public.php'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        rows = soup.find_all('tr')
        print_success("PowerReaper: Request Successful")
        return rows
    except:
        print_error("PowerReaper: request to the web page Failed!")
        return None


def get_row_data(rows):
    print_success("PowerReaper: Processing Rows...")
    maxIndex = 11
    excludedIndices = [0, 1, 7, 8, 10, 11]
    data = []
    try:
        for row in rows:
            if None in row:
                continue
            cols = row.find_all('td')
            colData = []
            for index, val in enumerate(cols):
                if (not index in excludedIndices):
                    if None in val:
                        colData.append('N/A')
                    else:
                        colData.append(val.text.strip())
                if(index == maxIndex):
                    data.append(power_data(colData))
        print_success("PowerReaper: Rows processing successful")
        return data
    except:
        print_error("PowerReaper: Rows processing Failed!")
        return []


def print_data(data):
    for datum in data:
        print(datum.division, datum.sub_division, datum.sub_station,
              datum.from_time, datum.to_time, datum.areas, sep=" --***-- ")


def write_to_file(data):
    print_success("PowerReaper: Initing Write to file")
    data_file = open("power_data.txt", "w+")
    try:
        print_success(
            "PowerReaper: Writing to file power_data.txt at you current directory...")
        for datum in data:
            data_file.write(
                "{division} --|***|-- {sub_division} --|***|-- {sub_station} --|***|-- {from_time} --|***|-- {to_time} --|***|-- {areas}--||**||--".format(division=datum.division, sub_division=datum.sub_division, sub_station=datum.sub_station, from_time=datum.from_time, to_time=datum.to_time, areas=datum.areas))
        print_success("PowerReaper: File write successful")
    except Exception as e:
        print_error("PowerReaper: Writing to file Failed!")
        print_error(e)
    finally:
        data_file.close()
        print_warning("PowerReaper: Data file closed...")
