# Description
Return a randomized lab that is applicable for the BSCP exam. For example, this does not include the labs where you need to get the leather jacket or labs of expert difficulty.
The [mystery lab](https://portswigger.net/web-security/mystery-lab-challenge) has given me these unwanted labs very often. So I decided to use my time wisely and create a tool that only serves labs that I deem useful.

The tool exists out of three parts:
- The Burp project file; Alters data in the HTTP traffic to hide the lab specific information like SQLi or XSS.
- Mitmdump; Alters data in the HTTP traffic to hide the lab specific information like SQLi or XSS.
- randomizer.py; this will gather all 'relevant' labs, return one at random and URL encoded.

# Disclaimer
Do keep in mind that I strongly recommend to do these 'skipped' labs regardless. Do *NOT* think this tool will be the only resource you need for the exam. This tool helps you to focus on the exam, it will not teach you the actual skill needed.

# Installation
Mandatory:
- [poetry](https://python-poetry.org/docs/#installation)
- [mitmproxy](https://docs.mitmproxy.org/stable/overview-installation/)

Optional, if you prefer FireFox over Burp browser/Chromium:
- [FireFox](https://www.mozilla.org/en-US/firefox/new/)
- [FoxyProxy](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/): Add an entry for 127.0.0.1:8080

Install the dependencies:

`$ poetry install`

# Running

`$ poetry run ./bscp_labs_randomizer/randomizer.py --help`

`$ poetry run ./bscp_labs_randomizer/randomizer.py update`

`$ poetry run ./bscp_labs_randomizer/randomizer.py list`

`$ poetry run ./bscp_labs_randomizer/randomizer.py random -p`

`$ burpsuite --project-file=randomizer.json`

Now copy the (encoded) URL that was generated and put it in the Burp browser (or Firefox).
Happy hacking!

# To do:
- Add vuln categories
- Exam step categories
- Keep track of last X
- Improve argparse
- Split the functions cleanly
- Integrate mitmdump as python

# Known bugs
- When creating the database it is not possible to appoint a location

# Formatting 
Formatting is done in [black](https://pypi.org/project/black/)

`$ python -m pip install black`

`$ black randomizer.py`
