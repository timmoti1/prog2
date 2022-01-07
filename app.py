import sqlite3
from typing import Text
from flask import Flask
from flask import render_template, send_from_directory, redirect, url_for, g, request
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

def write_db(query, args=()):
    """
    copy paste from above function with minor changes documented in flask documentation to be able to write to the db.
    """
    cur = get_db().execute(query, args)
    get_db().commit()
    cur.close()

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

    list_items = query_db("select * from todo where status = 0")
    backlog_list = []

    #convert results to dict per our own specifications
    for item in list_items:
        entry = dict()
        entry["taskid"] = item[0]
        entry["title"] = item[1]
        entry["description"] = item[2]
        entry["modified"] = item[3]
        
        backlog_list.append(entry)

    return render_template('index.html', page=0, items=backlog_list)

@app.route("/active")
def display_active():

    list_items = query_db("select * from todo where status = 1")
    active_list = []

    #convert results to dict per our own specifications
    for item in list_items:
        entry = dict()
        entry["taskid"] = item[0]
        entry["title"] = item[1]
        entry["description"] = item[2]
        entry["modified"] = item[3]
        
        active_list.append(entry)
    
    return render_template('index.html', page=1, items=active_list)

@app.route("/done")
def display_done():

    list_items = query_db("select * from todo where status = 2")
    done_list = []

    #convert results to dict per our own specifications
    for item in list_items:
        entry = dict()
        entry["taskid"] = item[0]
        entry["title"] = item[1]
        entry["description"] = item[2]
        entry["modified"] = item[3]
        
        done_list.append(entry)
    
    return render_template('index.html', page=2, items=done_list)

@app.route("/archived")
def display_archived():

    list_items = query_db("select * from todo where status = 3")
    archived_list = []

    #convert results to dict per our own specifications
    for item in list_items:
        entry = dict()
        entry["taskid"] = item[0]
        entry["title"] = item[1]
        entry["description"] = item[2]
        entry["modified"] = item[3]
        
        archived_list.append(entry)

    return render_template('index.html', page=3, items=archived_list)

@app.route("/edit", methods=["GET", "POST"])
def edit_note():

    if request.method == "POST":
        title = request.form.get("form_title")
        description = request.form.get("form_description")
        taskid = request.form.get("form_taskid", type=int)
        duedate = request.form.get("form_duedate")
        today_str = datetime.date.today().strftime("%Y-%m-%d")

        if taskid == 0:
            write_db("insert into todo (title, content, modification_date, due_date, status) values (?, ?, ?, ?, 0)", [title, description, today_str, duedate])
        
        else:
            write_db("update todo set title = ?, content = ?, modification_date = ?, due_date = ? where ID = ?", [title, description, today_str, duedate, taskid])
        
        return redirect(url_for("display_backlog"))

    
    task_id = request.args.get('tid', type=int)
    action_type = request.args.get('action', type=str)

    if action_type is not None:
        if action_type == "delete":
            write_db("delete from todo where ID = ?", [task_id])
        if action_type == "move":
            stat = query_db("select status from todo where ID = ?", [task_id], one=True)
            new_stat = int(stat[0]) + 1
            write_db("update todo set status = ? where ID = ?", [new_stat, task_id])

        return redirect(url_for("display_backlog"))

    fdat = dict()
    fdat["duedate"] = None
    fdat["title"] = None
    fdat["description"] = None
    fdat["taskid"] = 0

    if task_id is not None:
        task_data = query_db("select * from todo where ID = ?", [task_id], one=True)
        fdat["title"] = task_data[1]
        fdat["description"] = task_data[2]
        fdat["duedate"] = task_data[4]
        fdat["taskid"] = task_id

    return render_template('edit.html', fdat = fdat)

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