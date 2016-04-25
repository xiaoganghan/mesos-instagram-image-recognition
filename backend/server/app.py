import json
import urllib
import commands
from flask import Flask, request

app = Flask(__name__)


def rec_image(image_url):
    image_filepath = '/tmp/file.jpg'
    urllib.urlretrieve(image_url, image_filepath)
    output = commands.getstatusoutput('python classify_image.py --image_file {}'.format(image_filepath))
    objects = []
    for line in output[1].split('\n'):
        if line.find('(score =') > 0:
            objects.append(line)
    return objects


@app.route("/")
def recognize():
    if 'image_url' in request.args:
        image_url = request.args['image_url']
        objects = rec_image(image_url)
    else:
        objects = []

    data = {
        'objects': objects
    }
    return json.dumps(data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
