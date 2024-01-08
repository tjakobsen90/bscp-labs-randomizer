# https://mitmproxy.org/
# https://docs.mitmproxy.org/stable/addons-examples/#http-redirect-requests

from mitmproxy import http

def request(flow: http.HTTPFlow):
    # redirect to different host
    if flow.request.pretty_host == "web-security-academy.net":
        flow.request.host = "127.0.0.1:8081"
    # answer from proxy
    elif flow.request.path.endswith("/brew"):
    	flow.response = http.Response.make(
            418, b"I'm a teapot",
        )