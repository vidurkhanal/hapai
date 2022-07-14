import os
from urllib import response
import requests


def login(req):
    auth = req.authorization
    if not auth:
        return None, ("missing credentials", 401)
    basicAuth = (auth.username, auth.password)
    res = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", auth=basicAuth)
    if res.status_code == 200:
        return response.text, None
    else:
        return None, (res.text, res.status_code)
