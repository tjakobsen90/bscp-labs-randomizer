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
import random
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler(sys.stdout)],
)

parser = argparse.ArgumentParser(prog="ProgramName", description="What the program does", epilog="Text at the bottom of help")
parser.add_argument("option", help="random, list or update")
args = parser.parse_args()

def main(args):
    actions = {
        "random": {"func": random_lab},
        "list": {"func": list},
        "update": {"func": update},
    }
    result = actions.get(args.option)["func"]()

    if result:
        logging.info("Good luck!")
        quit()
    else:
        quit()

def random_lab():
    try:
        with open("database.links", "r") as file:
            urls = json.load(file)
    except Exception as e:
        logging.warning("Database file unavailable, did you create it with 'update'?")
        logging.warning(f"Message: {e}")
        return False
    print(urls)
    print(type(urls))
    res = random_number, random_url = random.choice(list(urls.items()))
    print(random_url)
    #.value())#.split("%2f")
    # for i in range(1, 4):
    #     url_random[i] = encode_all(url_random[i])
    #     url_encoded = "%2f".join(map(str, url_random))
    # logging.info(f"The URL is: {url_encoded}")
    # return True

def list():
    try:
        with open("database.links", "r") as file:
            pass
    except Exception as e:
        logging.warning("Database file unavailable, did you create it with 'update'?")
        logging.warning(f"Message: {e}")
        return False
    return True

def update():
    logging.info("Get some coffee, this will take a while")

    url_main = "https://portswigger.net"

    url_labs = f"{url_main}/web-security/all-labs"
    r_labs = requests.get(url_labs)
    link_labs = []
    numb = 0
    if r_labs.status_code == 200:
        soup = BeautifulSoup(r_labs.text, "html.parser")
        elements = soup.find_all(class_="widgetcontainer-lab-link")
        for element in elements:
            link_labs.append(element.find_all("a")[0].get("href"))
            if numb == 5:
                break
            numb += 1
    else:
        logging.error(f"The URL {url_labs} is unavailable")
        logging.error(f"Status code: {r_labs.status_code}")
        return False

    link_launches = []
    for link_lab in link_labs:
        r_launches = requests.get(f"{url_main}{link_lab}")
        if r_launches.status_code == 200:
            soup = BeautifulSoup(r_launches.text, "html.parser")
            elements = soup.find_all("a", class_="button-orange")
            for element in elements:
                link_launches.append(element["href"])
        else:
            logging.error(f"The URL {link_lab} is unavailable")
            logging.error(f"Status code: {r_launches.status_code}")
            return False
        # I don"t want an angry PortSwigger
        time.sleep(2)

    dict_launches = {}
    number = 0
    for link_launch in link_launches:
        dict_launches[number] = f"{url_main}{link_launch}"
        number += 1
    try:
        with open("database.links", "w") as file:
            json.dump(dict_launches , file)
    except Exception as e:
        logging.error("Can't create database file")
        logging.error(f"Message: {e}")
        return False
    return True


def encode_all(string):
    return "".join("%{0:0>2x}".format(ord(char)) for char in string)

if __name__ == "__main__":
    main(args)
