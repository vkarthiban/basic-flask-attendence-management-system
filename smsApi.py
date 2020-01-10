import http.client 

conn = http.client.HTTPSConnection("api.msg91.com")

payload = '''{
  "sender": "kunnel",
  "route": "4",
  "country": "91",
  "sms": [
    {
      "message": "your otp is 0007",
      "to": [
        "8610247456"
      ]
    },
  ]
}'''

headers = {
    'authkey': "280670AP5ubxbQ6Zm45d00a56a",
    'content-type': "application/json"
    }

conn.request("POST", "/api/v2/sendsms?country=91", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))