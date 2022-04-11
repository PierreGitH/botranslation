import requests
import json


def get_translation(text, target, source="auto"):

    search_api_url = "https://libretranslate.de/translate"
    headers = {"Content-Type": "application/json" }
    body = {'q': text,
                'source': source,
                'target': target
              }

    json_obj = json.dumps(body)

    response = requests.post(search_api_url, headers=headers, data=json_obj, timeout=5, )

    return json.loads(response.text)["translatedText"]

#
# translated = get_translation("Ceci est un test", "en", source="auto")
# print(translated)