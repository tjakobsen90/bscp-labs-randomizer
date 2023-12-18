#!/usr/bin/python3
# https://github.com/tjakobsen90/bscp-mystery-lab-randomizer

# Only randomize mystery labs that are applicable for the BSCP exam
# For example, this does not include the labs where you need to get the leather jacket for 1337 dollars

import argparse
import requests
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('filename')           # positional argument
parser.add_argument('-c', '--count')      # option that takes a value
parser.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag

# Define the URL you want to scrape
URL = "https://portswigger.net"

def main():
    args = parser.parse_args()
    print(args.filename, args.count, args.verbose)
    pass

def list():
    # List all the imported labs
    pass

def random():
    # Choose a random mystery lab
    pass

def update():
    # Send an HTTP GET request to the URL
    res = requests.get(URL+'/web-security/all-labs')
    labLinks = list()
    # Check if the request was successful (status code 200)
    if res.status_code == 200:
        # Parse the HTML content of the page using Beautiful Soup
        soup = BeautifulSoup(res.text, 'html.parser')
        labElements = soup.find_all(class_="widgetcontainer-lab-link")
        print(f"Count of Lab Elements: {len(labElements)}")

        for e in labElements:
            link = URL + e.find_all('a')[0].get('href')
            labLinks.append(link)
        print(f"Count of Lab Links: {len(labElements)}")
        print(labLinks)
    else:
        print("Failed to retrieve the web page. Status code:", res.status_code)

if __name__ == "__main__":
    main()