from flask import Flask
from os import path
from logging.config import fileConfig

app = Flask(__name__)

def get_base_file_path():
    return path.dirname(path.abspath(__file__))

log_file_path = path.join(get_base_file_path(), 'config/logging.config')
fileConfig(log_file_path)

@app.route('/')
def hello_world():
    app.logger.info('Processing default request')
    return 'Hello World!'

if __name__ == '__main__':
    app.run()