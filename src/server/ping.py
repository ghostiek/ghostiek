import requests
import json

x = requests.get("https://jellyfin.local:5000/getData", verify="certs/cert.pem")

print(json.loads(x.text))
