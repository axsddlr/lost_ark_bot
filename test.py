import requests

url = "https://nwdb.info/server-status/servers.json"

payload = ""
headers = {

    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/94.0.4606.61 Safari/537.36",
}

response = requests.request("GET", url, data=payload, headers=headers)

print(response.text)