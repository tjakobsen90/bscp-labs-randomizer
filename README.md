# Description
Only randomize mystery labs that are applicable for the BSCP exam. For example, this does not include the labs where you need to get the leather jacket or labs of expert difficulty.
The [mystery lab](https://portswigger.net/web-security/mystery-lab-challenge) has given me these unwanted labs very often. So I decided to use my time wisely and create a tool that serves 

# Disclaimer
Do keep in mind that I strongly recommend to do these 'skipped' labs regardless. Do *NOT* think this tool will be the only resource you need for the exam. This tool helps you focus on the exam, not the actual skill needed.

# Installation
Mandatory:
- [Poetry](https://python-poetry.org/docs/#installation)
- [mitmproxy](https://docs.mitmproxy.org/stable/overview-installation/)

Optional, if you prefer FireFox over Chromium:
- [FireFox](https://www.mozilla.org/en-US/firefox/new/)
- [FoxyProxy](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/): Add an entry for 127.0.0.1:8080

Install the dependencies:
`$ poetry install`

# Running
`$ poetry run ./bscp_labs_randomizer/randomizer.py --help`
`$ poetry run ./bscp_labs_randomizer/randomizer.py update`
`$ poetry run ./bscp_labs_randomizer/randomizer.py list`
`$ poetry run ./bscp_labs_randomizer/randomizer.py random -p`

Open up BurpSuite Pro and use the project file: `randomizer.json`
`$ burpsuite --project-file=randomizer.json`
Happy hacking!

# To do:
- add vuln categories switch
- Exam step categories
- Keep track of last X

# Known bugs
- When creating the database it is not possible to appoint a location

# Formatting 
Formatting is done in black: https://pypi.org/project/black/
`$ python -m pip install black`
`$ black randomizer.py`
