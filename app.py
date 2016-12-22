# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)



# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path,  'etchr.db' ),
    SECRET_KEY= "development key",
    USERNAME= "admin" ,
    PASSWORD= "default"
    ))
app.config.from_envvar( 'FLASKR_SETTINGS' , silent=True)

def connect_db():
    #"""Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the current application context.
    """
    if not hasattr(g,  'sqlite_db' ):
        g.sqlite_db = connect_db()
        return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g,  'sqlite_db' ):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource( 'schema.sql', mode= 'r' ) as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command( 'initdb' )
def initdb_command():
    """Initializes the database."""
    init_db()
    print  "Initialized the database."

@app.route( '/' )
def homepage():
    db = get_db()
    cur = db.execute( 'select title, text from entries order by id desc' )
    entries = cur.fetchall()
    return render_template( 'show_entries.html' , entries=entries)


@app.route( '/entries' )
def show_entries():
    db = get_db()
    cur = db.execute( 'select title, text from entries order by id desc' )
    entries = cur.fetchall()
    return render_template( 'show_entries.html' , entries=entries)

@app.route( '/entry/add' , methods=[ 'POST' ])
def add_entry():
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)' ,[request.form[ 'title' ], request.form[ 'text' ]])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route( '/persons' )
def show_persons():
    db = get_db()
    cur = db.execute( 'select * from person order by id desc' )
    items = cur.fetchall()
    return render_template( 'show_persons.html' , persons=items)

@app.route( '/person/add' , methods=[ 'POST' ])
def add_person():
    print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('insert into person (name, wageid,sex,title,category) values (?, ?,?,?,?)' ,[request.form[ 'name' ], request.form[ 'wageid' ],request.form['sex'],request.form['title'],request.form['category']])
    db.commit()
    print("commit")
    flash('New person was successfully inserted')
    return redirect(url_for('show_persons'))


@app.route( '/person/<int:person_id>/classtech_techer' )
def show_classtech_techer(person_id):
    db = get_db()
    cur = db.execute( 'select * from classtech_techer where person_id = ?',str(person_id) )
    items = cur.fetchall()
    return render_template( 'show_classtech_techer.html' , info={'items':items,'person_id':person_id})

@app.route( '/person/<int:person_id>/classtech_techer/add' , methods=[ 'POST' ])
def add_classtech_techer(person_id):
    print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('insert into classtech_techer (person_id,basictech_days,shortterm_days,totalwork_days,systemtraining_machanical_days,systemtraining_machanical_stucount,systemtraining_other_days,compulsorycourse_techhour,compulsorycourse_stucount,elective_techhour,elective_stucount,graduationproject_stucount,nuetiac_swjtu,nuetiac_sichuan,nuetiac_nation,make_techdays,note) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)' ,[person_id,request.form[ 'basictech_days' ],request.form['shortterm_days'],request.form['totalwork_days'],request.form['systemtraining_machanical_days'],request.form['systemtraining_machanical_stucount'],request.form['systemtraining_other_days'],request.form['compulsorycourse_techhour'],request.form['compulsorycourse_stucount'],request.form['elective_techhour'],request.form['elective_stucount'],request.form['graduationproject_stucount'],request.form['nuetiac_swjtu'],request.form['nuetiac_sichuan'],request.form['nuetiac_nation'],request.form['make_techdays'],request.form['note']])
    db.commit()
    print("commit")
    flash('New classtech_techer log was successfully inserted')
    return redirect(url_for('show_classtech_techer',person_id = person_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
