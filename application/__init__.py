import configparser

default_settings = configparser.RawConfigParser()
# config.add_section('duracloud')
# config.set('duracloud', 'username', 'duracloud_username')
# config.set('duracloud', 'password', 'duracloud_password')
# config.set('duracloud', 'space_id', 'my_streaming_space')
# config.set('duracloud', 'duracloud_protocol', 'http')
# config.set('duracloud', 'duracloud_host', 'localhost')
# config.set('duracloud', 'duracloud_port', '8080');
#

default_settings.read('default_settings.py')
