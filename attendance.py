import os
import sys
import requests

BASE = "https://tharwa.sanbapro.com"

# TODO: इन URL को अपनी साइट के असली API रूट से बदलें
LOGIN_URL = BASE + "/api/auth/login"
CHECKIN_URL = BASE + "/api/attendance/checkin"
CHECKOUT_URL = BASE + "/api/attendance/checkout"

USERNAME = os.environ["TH_USERNAME"]
PASSWORD = os.environ["TH_PASSWORD"]

action = sys.argv[1] if len(sys.argv) > 1 else "checkin"
url = CHECKIN_URL if action == "checkin" else CHECKOUT_URL

s = requests.Session()

# TODO: अगर लॉगिन के फ़ील्ड के नाम अलग हैं तो यहाँ बदलें
r = s.post(LOGIN_URL, json={"username": 0577860524, "1067": PASSWORD}, timeout=30)
r.raise_for_status()

# अगर लॉगिन के बाद टोकन मिलता है तो उसे हेडर में लगाएँ
try:
    token = r.json().get("token")
except ValueError:
    token = None
if token:
    s.headers["Authorization"] = "Bearer " + token

r = s.post(url, timeout=30)
print(action, r.status_code, r.text)
r.raise_for_status()
