import sqlite3
from typing import Text
from flask import Flask
from flask import render_template, send_from_directory
import datetime

DATABASE = 'database.db'

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route("/")
def default_route():
    """
    this is the default route, just like the "index.html" file of a website.
    """
    return render_template('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    """ Serves static JavaScript content """
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    """ Serves static CSS content """
    return send_from_directory('css', path)

@app.route('/img/<path:path>')
def send_media(path):
    """ Serves static Media content (images, or whatever is in that media folder) """
    return send_from_directory('img', path)

if __name__ == '__main__':
    app.run(debug=True)