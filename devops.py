import urllib.parse
url = "https://portswigger.net/academy/labs/launch/d9a071d8264e85184722707ff5747bbbd77963967d1d01f1b22f5dd8252f9767?referrer=%2fweb-security%2fsql-injection%2flab-retrieve-hidden-data"

def encode_all(string):
    return "".join("%{0:0>2x}".format(ord(char)) for char in string)
s = url.split("%2f")

for i in range(1, 4):
    s[i] = encode_all(s[i])
r = "%2f".join(map(str, s))

print(r)
