#!/usr/bin/python3
# https://github.com/tjakobsen90/bscp-mystery-lab-randomizer

# Only randomize mystery labs that are applicable for the BSCP exam
# For example, this does not include the labs where you need to get the leather jacket for 1337 dollars

import argparse
import requests
import logging
import time
import json
import sys
from bs4 import BeautifulSoup

url_main = "https://portswigger.net"


parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('action')           # positional argument
parser.add_argument('-c', '--count')      # option that takes a value
parser.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag
#args = parser.parse_args()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler(sys.stdout)],
)

def main():
    update()
    quit()

def list():
    # List all the imported labs
    pass

def random():
    # Choose a random mystery lab
    pass

def update():
    logging.info("Get some coffee, this will take a while")

    url_labs = f"{url_main}/web-security/all-labs"
    r_labs = requests.get(url_labs)

    link_labs = []
    if r_labs.status_code == 200:
        soup = BeautifulSoup(r_labs.text, 'html.parser')
        elements = soup.find_all(class_="widgetcontainer-lab-link")
        for element in elements:
            link_labs.append(element.find_all('a')[0].get('href'))
    else:
        logging.error(f"{url_labs} status code: {r_labs.status_code}")
        return

    link_launches = []
    for link_lab in link_labs:
        r_launches = requests.get(f"{url_main}{link_lab}")
        if r_launches.status_code == 200:
            soup = BeautifulSoup(r_launches.text, 'html.parser')
            elements = soup.find_all('a', class_="button-orange")
            for element in elements:
                link_launches.append(element['href'])
        else:
            logging.error(f"{link_lab} status code: {r_launches.status_code}")
            return
        # I don't want an angry PortSwigger
        time.sleep(1)

    dict_launches = {}
    number = 0
    for link_launch in link_launches:
        dict_launches[number] = f"{url_main}{link_launch}"
        number += 1
    with open("database.links", "w") as file:
        json.dump(dict_launches , file) 

if __name__ == "__main__":
    main()