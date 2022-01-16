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

def getTaskList(status):
    """
    This function gets the task list from DB, makes a dict out of the items and returns it. 
    Status parameter can be 0, 1, 2, 3 (backlog, active, done, archived)

    it also computes the time left per task in days.
    """
    list_items = query_db("select * from todo where status = ?", [status])
    task_list = []

    #convert results to dict per our own specifications
    for item in list_items:
        entry = dict()
        entry["taskid"] = item[0]
        entry["title"] = item[1]
        entry["description"] = item[2]
        entry["modified"] = item[3]

        #bugfix
        if item[4] is not "":
            due_date = datetime.datetime.strptime(item[4], "%Y-%m-%d").date() #parse date from database entry
            days_left = due_date - datetime.date.today() # calculate difference to today
        else:
            days_left = datetime.timedelta(days=10) #set days left to a bunch of days so that the badge won't be displayed
        
        if(days_left.days == 1):
            entry["due"] = True
            entry["due_color"] = "bg-warning"
            entry["due_text"] = "Due Tomorrow"
        
        if(days_left.days == 0):
            entry["due"] = True
            entry["due_color"] = "bg-warning"
            entry["due_text"] = "Due Today"
        
        if(days_left.days < 0):
            entry["due"] = True
            entry["due_color"] = "bg-danger"
            entry["due_text"] = "Overdue"
        
        
        task_list.append(entry)
    
    return task_list

@app.route("/")
def default_route():
    """
    this is the default route, just like the "index.html" file of a website.
    """
    return redirect(url_for("display_backlog"))

@app.route("/backlog")
def display_backlog():

    backlog_list = getTaskList(0)

    return render_template('index.html', page=0, items=backlog_list)

@app.route("/active")
def display_active():

    active_list = getTaskList(1)
    
    return render_template('index.html', page=1, items=active_list)

@app.route("/done")
def display_done():

    done_list = getTaskList(2)
    
    return render_template('index.html', page=2, items=done_list)

@app.route("/archived")
def display_archived():

    archived_list = getTaskList(3)

    return render_template('index.html', page=3, items=archived_list)

@app.route("/edit", methods=["GET", "POST"])
def edit_note():
    """
    edits the note if it already exists or creates it if it does not exist.
    if it exists, data from DB will be passed to the template to see the current information on the task.
    """

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

    pbar = dict()
    stat_num = list()

    for i in range(4):
        li = query_db("select * from todo where status = ?", [i])
        stat_num.append(len(li))

    total = sum(stat_num)

    print(stat_num)

    pbar["backlog"] = stat_num[0]/total * 100
    pbar["active"] = stat_num[1]/total * 100
    pbar["done"] = stat_num[2]/total * 100
    pbar["archived"] = stat_num[3]/total * 100

    print(pbar)

    return render_template('statistics.html', pbar=pbar, sta=stat_num)

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