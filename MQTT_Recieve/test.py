import requests

# Replace {type} with the actual type of data you want to retrieve.
# Replace YOUR_ACCESS_KEY with your actual access key.
url = "https://nam1.cloud.thethings.network/api/v3/as/applications/lora-fyp-testing-2023-24/packages/storage/uplink_message"

headers = {
    "Authorization": "NNSXS.G76CW7MEHL57Z63EGZ37B3F5NC5XBVZAAIIJR2I.ZMWJLERLEGLILKMGNDNKSPC32OWKOBXIV2N6CGCZWHX652YSAZKQ"
}

response = requests.get(url, headers=headers)

print(response.text)
