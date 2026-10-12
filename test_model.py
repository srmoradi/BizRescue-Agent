
import os
import json
import urllib.request
import urllib.error

API_KEY = os.environ.get("LITELLM_API_KEY")

if not API_KEY:
    print("ERROR: LITELLM_API_KEY is not set.")
    raise SystemExit(1)

url = "https://litellm.vision.aivar.app/v1/chat/completions"

payload = {
    "model": "nova-micro",
    "messages": [
        {
            "role": "user",
            "content": "Reply with exactly: Avin AI model test successful."
        }
    ],
    "max_tokens": 40
}

request = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(request, timeout=45) as response:
        result = json.loads(response.read().decode("utf-8"))
        print("HTTP:", response.status)
        print("MODEL:", result.get("model", "unknown"))
        print("REPLY:", result["choices"][0]["message"]["content"])

except urllib.error.HTTPError as error:
    print("HTTP ERROR:", error.code)
    print(error.read().decode("utf-8")[:1500])

except Exception as error:
    print("ERROR:", str(error))
