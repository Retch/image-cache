import os
import time
import threading
import requests
from flask import Flask, send_file, abort
from io import BytesIO

app = Flask(__name__)

IMAGE_URL = str(os.getenv('SOURCE_URL', 'https://picsum.photos/1920/1080'))
CACHE_NAME = str(os.getenv('CACHE_NAME', 'cache'))
MIN_IMAGE_SIZE = int(os.getenv('MIN_CONTENT_BYTES', 10240))

in_memory_image = None

def download_image():
    global in_memory_image
    while True:
        try:
            response = requests.get(IMAGE_URL, timeout=5)
            if response.status_code == 200 and len(response.content) >= MIN_IMAGE_SIZE:
                in_memory_image = BytesIO(response.content)
                print("Picture saved in memory")
            else:
                print(f"Image not available for download, code {response.status_code}")
        except requests.RequestException as e:
            print(f"Image not available for download {e}")
        time.sleep(0.1)

@app.route('/' + CACHE_NAME)
def view_image_endpoint():
    global in_memory_image
    if in_memory_image:
        image_copy = BytesIO(in_memory_image.getvalue())
        return send_file(image_copy, mimetype='image/jpeg')
    else:
        abort(503, description="Image not available yet")

if __name__ == '__main__':
    downloader_thread = threading.Thread(target=download_image)
    downloader_thread.daemon = True
    downloader_thread.start()

    app.run(debug=True, host='0.0.0.0', port=5000)
