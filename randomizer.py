#!/usr/bin/python3
# https://github.com/tjakobsen90/bscp-mystery-lab-randomizer

# Only randomize mystery labs that are applicable for the BSCP exam
# For example, this does not include the labs where you need to get the leather jacket
# Do keep in mind that I strongly recommend to do these 'skipped' labs regardless

# To do:
# - Vuln categories
# - Exam step categories

import argparse
import requests
import logging
import time
import json
import sys
import random
from bs4 import BeautifulSoup

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s",
    handlers = [logging.FileHandler("debug.log"), logging.StreamHandler(sys.stdout)],
)

parser = argparse.ArgumentParser(prog="randomizer", description="Returns a random BSCP lab that is applicable for the BSCP exam")
parser.add_argument("option", help="random, list or update")
args = parser.parse_args()

blacklist = [
    "oracle",
    "bypass"
]

def main(args):
    logging.info("BSCP Labs Randomizer")
    actions = {
        "random": {"func": random_lab},
        "list": {"func": list},
        "update": {"func": update },
    }

    if actions.get(args.option)["func"]():
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

    # random needs improvement
    url_random = random.sample(urls.items(), 1)[0][1].split("%2f")
    for i in range(1, len(url_random)):
        url_random[i] = encode_all(url_random[i])
        url_encoded = "%2f".join(map(str, url_random))
    logging.info(f"The URL is: {url_encoded}")

    return True

def list():
    try:
        with open("database.links", "r") as file:
            urls = json.load(file)
    except Exception as e:
        logging.warning("Database file unavailable, did you create it with 'update'?")
        logging.warning(f"Message: {e}")
        return False

    logging.info("The current entries in the database are:")
    for number, url in urls.items():
        logging.info(f"{number}: {url}")

    return True

def update():
    logging.info("Get some coffee, this will take a while")

    url_main = "https://portswigger.net"

    labs_urls = f"{url_main}/web-security/all-labs"
    r_labs = requests.get(labs_urls)
    labs_links = []
    if r_labs.status_code == 200:
        soup = BeautifulSoup(r_labs.text, "html.parser")
        elements = soup.find_all(class_="widgetcontainer-lab-link")
        for element in elements:
            labs_links.append(element.find_all("a")[0].get("href"))
    else:
        logging.error(f"The URL {labs_urls} is unavailable")
        logging.error(f"Status code: {r_labs.status_code}")
        return False

    white_links = []
    for lab in labs_links:
        if not any(substring in lab for substring in blacklist):
            white_links.append(lab)

    launches = []
    for white in white_links:
        r_launches = requests.get(f"{url_main}{white}")
        if r_launches.status_code == 200:
            soup = BeautifulSoup(r_launches.text, "html.parser")
            elements = soup.find_all("a", class_="button-orange")
            for element in elements:
                launches.append(element["href"])
        else:
            logging.error(f"The URL {white} is unavailable")
            logging.error(f"Status code: {r_launches.status_code}")
            return False
        # I don"t want an angry PortSwigger
        time.sleep(2)

    dict_launches = {}
    number = 0
    for launch in launches:
        dict_launches[number] = f"{url_main}{launch}"
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
