import json
import time
import requests
from PIL import Image
from io import BytesIO
import base64

class Kadninsky_impl:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


if __name__ == '__main__':
    api = Kadninsky_impl('https://api-key.fusionbrain.ai/', '588158C56C8F10CEFF2D0D3B18F01619', '88EF9C3B72EFA6061718AD88C468D36B')
    model_id = api.get_model()
    input = str(input("Enter text: "))
    uuid = api.generate(input, model_id)
    images = api.check_generation(uuid)
    print(images)
    image_bytes = base64.b64decode(images[0])
    image = Image.open(BytesIO(image_bytes))
    image.save('image.png', format='PNG')
