import os
import requests


def token(req):
    if not "Authorization" in req.headers:
        return None, ("missing credentials,401")

    token = req.headers["Authorization"]

    if not token:
        return None, ("missing credentials", 401)

    res = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate", headers={"Authorization": token})

    if res.status_code == 200:
        return res.text, None
    else:
        return None, (res.text, res.status_code)
