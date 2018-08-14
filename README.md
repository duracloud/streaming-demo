# Streaming Demo

## Getting started

1. Install python 3 if it is not already installed.
2. Install virtualenv.
3. In the project directory create a virtual environment

    ```
    python3 -m venv venv
    ```
4. Activate the environment
    ```
    . venv/bin/activate
    ```
        
    or in windows
    
    ```
    venv\Scripts\activate
    ```

5. Install pre-requisites and the program.

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
# external hostname and port for the application
SERVER_NAME = "my-streaming-demo.example.org:5000"   
```
## Run the application
```
STREAMING_DEMO_SETTINGS=/your/path/myconfig.py FLASK_APP=application/app.py
 flask run --host=0.0.0.0
```

## Navigate to the video list
http://my-streaming-demo.example.org:5000/
