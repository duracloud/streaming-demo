# Streaming Demo

## Getting started
Install virtualenv
In the project directory create a virtual environment
```
python3 -m venv venv
```
Activate the environment
```
. venv/bin/activate
```
    
or in windows

```
venv\Scripts\activate
```

Install pre-requisites and the program.

```
pip install Flask
pip install requests
python setup.py install
```

## Define a config file
Create a file at /your/path/myconfig.py that contains the following keys, 
replacing the values with the values you want.

```
DURACLOUD_USERNAME = "duracloud_user"
DURACLOUD_PASSWORD = "duracloud_password"
DURACLOUD_SPACE_ID = "my_streaming_space"
DURACLOUD_PROTOCOL = "http"
DURACLOUD_HOST = "localhost"
DURACLOUD_PORT = "8080"
```
## Run the application
```
STREAMING_DEMO_SETTINGS=~/tmp/streaming-demo.py FLASK_APP=application/app.py flask run
```

## Navigate to the video list
http://localhost:5000/
