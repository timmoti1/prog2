import sqlite3
from typing import Text
from flask import Flask
from flask import render_template, send_from_directory, redirect, url_for, g
import datetime

DATABASE = 'database.db'

def get_db():
    """
    Flask SQLite3 connector
    (code taken from Flask documentation)
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

testitems=[
    {"title": "bla", "description": "boo"}
]

app = Flask(__name__)
app.secret_key = 'hey i am very secure'

@app.route("/")
def default_route():
    """
    this is the default route, just like the "index.html" file of a website.
    """
    return redirect(url_for("display_backlog"))

@app.route("/backlog")
def display_backlog():
    return render_template('index.html', page=0, items=testitems)

@app.route("/active")
def display_active():
    return render_template('index.html', page=1)

@app.route("/done")
def display_done():
    return render_template('index.html', page=2)

@app.route("/archived")
def display_archived():
    return render_template('index.html', page=3)

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