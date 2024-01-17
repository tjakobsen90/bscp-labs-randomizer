#!/usr/bin/python3
# https://github.com/tjakobsen90/bscp-labs-randomizer

import argparse
import json
import logging
import os
import random
import requests
import signal
import sys
import time
from bs4 import BeautifulSoup
from pathlib import Path

# Global variables
dbfile = "database.dict"
denyfile = "deny.list"

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


# parser.add_argument("random", help="Return a random lab from the database")
# parser.add_argument("list", help="Show all labs in the database")
# parser.add_argument("update", help="Update the database of labs")
# parser.add_argument("proxy", help="Run mitmdump on localhost:8080")
# --file

# Argument parser
parser = argparse.ArgumentParser(
    prog="randomizer",
    description="Returns a random BSCP lab that is applicable for the BSCP exam",
)
parser.add_argument("option", help="random, list, update or proxy")
parser.add_argument("-s", "--show", action="store_true", help="Show corresponding number of the random lab")
parser.add_argument("-p", "--proxy", action="store_true", help="Run mitmdump on localhost:8080")

args = parser.parse_args()

def main(args):
    logging.info("BSCP Labs Randomizer")

    actions = {
        "random": {"func": random_lab},
        "list": {"func": list_database},
        "update": {"func": update_database},
        "proxy": {"func": proxy_start},
    }

    if args.option in actions.keys():
        logging.info(f"Your choice: {args.option}")
        actions.get(args.option)["func"](args)
        logging.info("Goodbye!")
        quit()
    else:
        logging.warning("No valid option provided, use -h or --help")
        quit()


# Returns a random encoded lab URL
def random_lab(args):
    try:
        with open(dbfile, "r") as file:
            urls = json.load(file)
    except Exception as e:
        logging.warning("Database file unavailable, did you create it with 'update'?")
        logging.warning(f"Message: {e}")
        return False

    random_choice = random.choice(list(urls.items()))
    random_url = random_choice[1].split("%2f")
    random_number = random_choice[0]

    if args.show:
        logging.info(f"Number: {random_number}")

    for i in range(1, len(random_url)):
        random_url[i] = encode_all(random_url[i])
        url_encoded = "%2f".join(map(str, random_url))
    logging.info(f"URL: {url_encoded}")
    logging.info("Make sure you are logged in, copy/paste the URL to start")
    logging.info("Good luck!")

    if args.proxy:
        proxy_start()

    return True


# Shows all entries in the database file
def list_database():
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


# Creates and overwrites the database file
def update_database():
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
        with open(denyfile, "r") as file:
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


# Run the mitmdump command to alter the HTTP traffic
def proxy_start():
    signal.signal(signal.SIGINT, signal_handler)
    logging.info("Starting the proxy")
    logging.info("To exit press CTRL+C")
    args = '-k --modify-body ":~s:<h2>.*</h2>:<h2>BSCP Randomizer</h2>" --modify-body ":~s:<title>.*</title>:<title>BSCP Randomizer</title>" --modify-body ":~s:<title>.*</title>:<title>BSCP Randomizer</title>" --modify-body ":~s:<a class=link-back href=\'[^\n]*\'>:<a class=link-back href=\'https://www.youtube.com/watch?v=dQw4w9WgXcQ\'>"'
    try:
        os.system(f"mitmdump {args}")
    except Exception as e:
        logging.error("Can't start mitmdump")
        logging.error(f"Message: {e}")


# Encode characters URL style
def encode_all(string):
    return "".join("%{0:0>2x}".format(ord(char)) for char in string)


# Capture key strokes (CTRL+C)
def signal_handler(sig, frame):
    print("Exiting the proxy...")
    sys.exit(0)


# Run me :)
if __name__ == "__main__":
    main(args)
