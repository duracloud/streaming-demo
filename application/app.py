from flask import Flask
from flask import render_template, redirect, send_from_directory
import requests, json, os
import xml.etree.ElementTree as etree

app = Flask(__name__)

app.config.from_object('application.default_settings')

settings_env = 'STREAMING_DEMO_SETTINGS'
if os.environ.get(settings_env, default=None) is not None:
    app.config.from_envvar(settings_env)

def get_prop(key):
    return app.config.get(key)

def get_auth():
    return (get_prop("DURACLOUD_USERNAME"),get_prop("DURACLOUD_PASSWORD"))

def get_space_id():
    return get_prop("DURACLOUD_SPACE_ID")
@app.route("/")
def index():
    auth = get_auth()
    space_id = get_space_id()
    task_params = {'spaceId' : space_id}

    # get signed cookies
    auth = get_auth()
    r = requests.post(get_duracloud_base_url() +
                      "/task/get-signed-cookies",
                      data=json.dumps(task_params), auth=auth)
    signed_cookies = r.json()

    #get streaming host
    streaming_host = get_streaming_host()

    # add streaming host
    signed_cookies['streamingHost'] = streaming_host
    # add redirect url
    signed_cookies['redirectUrl'] = "http://" + get_prop("SERVER_NAME") + "/video-list" 

    # store signed cookies in durastore
    #change this value to duracloud store cookies url
    store_cookies_url = get_duracloud_base_url() + "/task/store-signed-cookies"
    r = requests.post(store_cookies_url,
                      json=signed_cookies,  auth=auth)

    token = r.json()['token'];
    print("token returned = " + token);

    #redirect to cloudfront set cookies url
    cloudfront_set_cookies_url = "https://" + streaming_host + \
                                 "/cookies?token=" \
                                 + token

    print("redirecting to " + cloudfront_set_cookies_url)
    return redirect(cloudfront_set_cookies_url)

def get_streaming_host():
    r = requests.get(get_duracloud_base_url() + "/" + get_space_id(), auth=get_auth())
    streaming_host = r.headers.get("x-dura-meta-hls-streaming-host")
    print("Streaming host = " + streaming_host)
    return streaming_host

def get_duracloud_base_url():
    return get_prop("DURACLOUD_PROTOCOL") + "://" + get_prop("DURACLOUD_HOST") + ":" + \
           get_prop("DURACLOUD_PORT") + "/durastore";

@app.route("/video-list")
def video_list():

    resp = requests.get(get_duracloud_base_url() + "/" + get_space_id(),
                 auth=get_auth())

    root = etree.fromstring(resp.content)
    items = []

    for item in root:
        if item.text.endswith("playlist.m3u8"):
            items.append(item.text)

    return render_template('video-list.html', items=items)

@app.route("/viewer/<videoId>")
def viewer(videoId=None):

    streaming_host = get_streaming_host()

    return render_template('viewer.html',
                           streaming_host=streaming_host, videoId=videoId)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)



