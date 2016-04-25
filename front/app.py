import time
from multiprocessing.dummy import Pool as ThreadPool

from flask import Flask, request
from flask import render_template

import requests
from instagram import extract_user_posts
app = Flask(__name__)

backend_vip_endpoint = 'http://1.2.3.4:5123'
# backend_vip_endpoint = 'http://192.168.99.100:5000'
worker_num = 16


def recognize(image_url):
    url = '{}/?image_url={}'.format(backend_vip_endpoint, image_url)
    ret = requests.get(url)
    if ret.status_code == 200:
        data = ret.json()
        objects = data['objects']
    else:
        objects = []
    return (image_url, objects)


@app.route("/", methods=['POST', 'GET'])
def homepage():
    if request.method == 'POST':
        username = request.form.get('username')
        posts = extract_user_posts(username)

        start = time.time()

        image_urls = [post['display_src'] for post in posts][:6]
        pool = ThreadPool(worker_num)
        results = pool.map(recognize, image_urls)
        pool.close()
        pool.join()

        total_seconds = time.time() - start

        return render_template(
            'index.html',
            username=username,
            images=results,
            total_seconds=total_seconds)

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
