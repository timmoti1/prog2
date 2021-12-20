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

def query_db(query, args=(), one=False):
    """
    Taken from Flask documentation. Example on how to query the DB (single and multi-row results posible)
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

app = Flask(__name__)
app.secret_key = 'hey bob, this is my secret love letter to you.' #what alice might have said, but eve would not understand it.

@app.route("/")
def default_route():
    """
    this is the default route, just like the "index.html" file of a website.
    """
    return redirect(url_for("display_backlog"))

@app.route("/backlog")
def display_backlog():

    list_items = query_db("select * from todo")
    backlog_list = []

    print(list_items)

    #convert results to dict per our own specifications
    for item in list_items:
        entry = dict()
        entry["title"] = item[1]
        entry["description"] = item[2]
        
        backlog_list.append(entry)

    return render_template('index.html', page=0, items=backlog_list)

@app.route("/active")
def display_active():
    return render_template('index.html', page=1)

@app.route("/done")
def display_done():
    return render_template('index.html', page=2)

@app.route("/archived")
def display_archived():
    return render_template('index.html', page=3)

@app.route("/stats")
def statisitcs():
    """
    Display statistics (how many items are in what category)
    Possible categories: backlog, active, donw, archived.

    This function gets all items from DB and calculates the percentage per category and passes a dict to template.
    """


    return render_template('statistics.html', pbar={"backlog": 10, "active": 10, "done": 10, "archived": 10})

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