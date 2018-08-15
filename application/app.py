from flask import Flask
from flask import render_template, redirect, send_from_directory, session, url_for
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

def has_configured_cookies():
    return session.get("has_cookies", False)

def configure_cookies(redirect_path):
    auth = get_auth()
    space_id = get_space_id()
    redirect_url = "http://" + get_prop("SERVER_NAME") + \
                                    redirect_path

    task_params = {'spaceId' : space_id, "redirectUrl" : redirect_url}

    r = requests.post(get_duracloud_base_url() + "/task/get-signed-cookies-url",
                      json=task_params,  auth=auth)

    signed_cookies_url = r.json()['signedCookiesUrl'];

    print("signed_cookies_url=" + signed_cookies_url)
    session.update({'has_cookies': True })
    return redirect(signed_cookies_url)

def get_streaming_host():
    r = requests.get(get_duracloud_base_url() + "/" + get_space_id(), auth=get_auth())
    streaming_host = r.headers.get("x-dura-meta-hls-streaming-host")
    print("Streaming host = " + streaming_host)
    return streaming_host

def get_duracloud_base_url():
    return get_prop("DURACLOUD_PROTOCOL") + "://" + get_prop("DURACLOUD_HOST") + ":" + \
           get_prop("DURACLOUD_PORT") + "/durastore";


@app.route("/")
def video_list():
    if not has_configured_cookies():
        return configure_cookies('/')


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
    if not has_configured_cookies():
        return configure_cookies('/viewer/' + videoId)

    streaming_host = get_streaming_host()

    return render_template('viewer.html',
                           streaming_host=streaming_host, videoId=videoId)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)



