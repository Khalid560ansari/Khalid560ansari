import os
import sys
import requests

BASE = "https://tharwa.sanbapro.com"

# ये तीनों URL अंदाज़े वाले हैं, असली API से बदलने होंगे
LOGIN_URL = BASE + "/api/auth/login"
CHECKIN_URL = BASE + "/api/attendance/checkin"
CHECKOUT_URL = BASE + "/api/attendance/checkout"

USERNAME = os.environ["TH_USERNAME"]
PASSWORD = os.environ["TH_PASSWORD"]

action = sys.argv[1] if len(sys.argv) > 1 else "checkin"
url = CHECKIN_URL if action == "checkin" else CHECKOUT_URL

s = requests.Session()

r = s.post(
    LOGIN_URL,
    json={"username": USERNAME, "password": PASSWORD},
    timeout=30,
)
print("login", r.status_code, r.text[:200])
r.raise_for_status()

try:
    token = r.json().get("token")
except ValueError:
    token = None
if token:
    s.headers["Authorization"] = "Bearer " + token

r = s.post(url, timeout=30)
print(action, r.status_code, r.text)
r.raise_for_status()
