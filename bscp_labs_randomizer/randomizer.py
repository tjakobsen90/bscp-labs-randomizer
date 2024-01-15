#!/usr/bin/python3
# https://github.com/tjakobsen90/bscp-labs-randomizer

# Only randomize mystery labs that are applicable for the BSCP exam
# For example, this does not include the labs where you need to get the leather jacket
# Do keep in mind that I strongly recommend to do these 'skipped' labs regardless

# Formatting is done in black: https://pypi.org/project/black/

# To do:
# - point to deny/db file
# - MitMProxy
# - Vuln categories
# - Exam step categories
# - Keep track of last X

import argparse
import requests
import logging
import time
import json
import sys
import random
import os
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

parser = argparse.ArgumentParser(
    prog="randomizer",
    description="Returns a random BSCP lab that is applicable for the BSCP exam",
)
parser.add_argument("option", help="random, list, update or runproxy")
args = parser.parse_args()


def main(args):
    logging.info("BSCP Labs Randomizer")
    actions = {
        "random": {"func": random_lab},
        "list": {"func": list},
        "update": {"func": update},
        "runproxy": {"func": runproxy}
    }

    if actions.get(args.option)["func"]():
        logging.info("Good luck!")
        quit()
    else:
        quit()


def random_lab():
    try:
        with open("database.dict", "r") as file:
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
    logging.info("Make sure you are logged in, copy/paste the URL to start")

    return True


def list():
    try:
        with open("database.dict", "r") as file:
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

    try:
        with open("deny.list", "r") as file:
            denylist = file.read().splitlines()
    except Exception as e:
        logging.warning("Deny file unavailable")
        logging.warning(f"Message: {e}")
        return False

    allowlist = []
    for lab in labs_links:
        if not any(substring in lab for substring in denylist):
            allowlist.append(lab)

    launches = []
    for allow in allowlist:
        r_launches = requests.get(f"{url_main}{allow}")
        if r_launches.status_code == 200:
            soup = BeautifulSoup(r_launches.text, "html.parser")
            elements = soup.find_all("a", class_="button-orange")
            for element in elements:
                launches.append(element["href"])
        else:
            logging.error(f"The URL {allow} is unavailable")
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
        with open("database.dict", "w") as file:
            json.dump(dict_launches, file)
    except Exception as e:
        logging.error("Can't create database file")
        logging.error(f"Message: {e}")
        return False

    return True

def runproxy():
    args = '-k --modify-body ":~s:<h2>.*</h2>:<h2>BSCP Randomizer</h2>" --modify-body ":~s:<title>.*</title>:<title>BSCP Randomizer</title>" --modify-body ":~s:<title>.*</title>:<title>BSCP Randomizer</title>" --modify-body ":~s:<a class=link-back href=\'[^\n]*\'>:<a class=link-back href=\'https://www.youtube.com/watch?v=dQw4w9WgXcQ\'>"'
    os.system(f"mitmdump {args}")

def encode_all(string):
    return "".join("%{0:0>2x}".format(ord(char)) for char in string)


if __name__ == "__main__":
    main(args)
