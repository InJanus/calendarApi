# this is the api for the control of the tasks and the calendar. 
# calendar days neet to have, month, day, year, and time.
# i need to be able to get from this info, day of the week.

#i need to create events with times and store them in a database.
#it would be nice to visulize it in calendar frormation, get events in google calendar to transfer, remind me when events are.

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from sqlite3 import Error
import json

app = Flask(__name__)
CORS(app)

def connectDB(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_task(conn, task, tablename):
    sql = "INSERT INTO " + tablename + " VALUES(\'" + task[0] + "\',\'" + task[1] + "\',\'" + task[2] + "\',\'" + task[3] + "\')"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def deleteAll_task(conn, tablename):
    cur = conn.cursor()
    cur.execute('DELETE FROM ' + tablename)
    conn.commit()

def ret_task(conn, tablename):
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + tablename)
    rows = cur.fetchall()

    col = []
    for row in cur.description:
        col.append(row[0])

    retval = {tablename:{}}
    count = 0
    for row in rows:
        mylist = {count: {}}
        for i in range(4):
            myinput = {col[i]:row[i]}
            mylist[count].update(myinput)
        retval[tablename].update(mylist)
        count = count + 1
    return retval

def tablenames(conn):
    cur = conn.cursor()
    cur.execute('SELECT name FROM sqlite_master WHERE type=\'table\'')
    tablenames = cur.fetchall()
    mylist = {'lists': {}}
    for i in range(len(tablenames)):
        mylist['lists'].update({i:tablenames[i]})
    mylist.update({'length':len(tablenames)})
    return mylist

def tabledelete(conn, tablename):
    cur = conn.cursor()
    cur.execute('DROP TABLE ' + tablename)
    conn.commit()
    return {'status':'Table Deleted'}

def tablenew(conn, tablename):
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ' + tablename + '(title STRING, disc STRING, date STRING, done STRING)')
    conn.commit()
    return {'status':'Table ' + tablename + ' created'}

@app.route('/api/1.0/tasksget/', methods=['GET'])
def get_tasks():
    connect = connectDB("data/info")
    tablename = request.args.get('table')
    return jsonify(ret_task(connect, tablename))

@app.route('/api/1.0/tablenames/', methods=['GET'])
def gettablenames():
    connect = connectDB("data/info")
    return jsonify(tablenames(connect))

@app.route("/api/1.0/tasksput/", methods=['PUT'])
def post_tasks():
    connect = connectDB("data/info")
    print(request.form)
    newtask = (request.form['title'], request.form['disc'], request.form['date'], request.form['done'])
    tablename = request.form['table']
    create_task(connect, newtask, tablename)
    return jsonify({'status':"Done"})

@app.route("/api/1.0/taskdeleteAll/", methods=['DELETE'])
def delete_tasks():
    connect = connectDB("data/info")
    tablename = request.args.get('table')
    deleteAll_task(connect, tablename)
    return jsonify({'status':"Done"})

@app.route("/api/1.0/tabledelete/", methods=['DELETE'])
def delete_table():
    connect = connectDB("data/info")
    tablename = request.args.get('table')
    return jsonify(tabledelete(connect, tablename))

@app.route("/api/1.0/tablenew/", methods=['PUT'])
def new_table():
    connect = connectDB("data/info")
    tablename = request.form['table']
    return jsonify(tablenew(connect, tablename))

if __name__ == '__main__':
    app.run(debug=True)