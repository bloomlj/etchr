#coding:utf-8
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
    return render_template( 'index.html' , entries=entries)


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

@app.route( '/persons_actions' )
def show_persons_actions():
    db = get_db()
    cur = db.execute( 'select * from person order by id desc' )
    items = cur.fetchall()
    return render_template( 'show_persons_actions.html' , persons=items)

@app.route( '/person/add' , methods=[ 'POST' ])
def add_person():
    #print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('insert into person (name, wageid,sex,title,category) values (?, ?,?,?,?)' ,[request.form[ 'name' ], request.form[ 'wageid' ],request.form['sex'],request.form['title'],request.form['category']])
    db.commit()
    print("commit")
    flash('New person was successfully inserted')
    return redirect(url_for('show_persons'))

@app.route( '/person/<int:person_id>/del' , methods=[ 'get' ])
def del_person(person_id):
    #print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('DELETE from  person  where id = ?' ,(person_id,) )
    db.commit()
    print("commit")
    flash('A person was successfully DELETED')
    return redirect(url_for('show_persons'))


@app.route( '/person/<int:person_id>/classtech_teacher' )
def show_classtech_teacher(person_id):
    db = get_db()
    cur = db.execute( 'select * from classtech_teacher where person_id = ?',(person_id,) )
    items = cur.fetchall()
    return render_template( 'show_classtech_teacher.html' , info={'items':items,'person_id':person_id})

@app.route( '/person/<int:person_id>/classtech_teacher/add' , methods=[ 'POST' ])
def add_classtech_teacher(person_id):
    #print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('insert into classtech_teacher (person_id,basictech_days,shortterm_days,totalwork_days,systemtraining_machanical_days,systemtraining_machanical_stucount,systemtraining_other_days,compulsorycourse_techhour,compulsorycourse_factor,compulsorycourse_stucount,elective_techhour,elective_isnew,elective_stucount,graduationproject_stucount,nuetiac_plan,nuetiac_make,nuetiac_swjtu,nuetiac_sichuan,nuetiac_nation,make_techdays,note) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)' ,[person_id,request.form[ 'basictech_days' ],request.form['shortterm_days'],request.form['totalwork_days'],request.form['systemtraining_machanical_days'],request.form['systemtraining_machanical_stucount'],request.form['systemtraining_other_days'],request.form['compulsorycourse_techhour'],request.form['compulsorycourse_factor'],request.form['compulsorycourse_stucount'],request.form['elective_techhour'],request.form['elective_isnew'],request.form['elective_stucount'],request.form['graduationproject_stucount'],request.form['nuetiac_plan'],request.form['nuetiac_make'],request.form['nuetiac_swjtu'],request.form['nuetiac_sichuan'],request.form['nuetiac_nation'],request.form['make_techdays'],request.form['note']])
    db.commit()
    print("commit")
    flash('New classtech_teacher log was successfully inserted')
    return redirect(url_for('show_classtech_teacher',person_id = person_id))

@app.route( '/person/<int:person_id>/classtech_teacher/<int:id>/del' , methods=[ 'get' ])
def del_classtech_teacher(person_id,id):
    #print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('DELETE from classtech_teacher  where id = ?' ,(id,) )
    db.commit()
    print("commit")
    flash('A log was successfully DELETED')
    return redirect(url_for('show_classtech_teacher',person_id=person_id))

@app.route( '/person/<int:person_id>/afterclass_teacher' )
def show_afterclass_teacher(person_id):
    db = get_db()
    cur = db.execute( 'select * from afterclass_teacher where person_id = ?',(person_id,) )
    items = cur.fetchall()
    return render_template( 'show_afterclass_teacher.html' , info={'items':items,'person_id':person_id})

@app.route( '/person/<int:person_id>/afterclass_teacher/add' , methods=[ 'POST' ])
def add_afterclass_teacher(person_id):
    #print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('insert into afterclass_teacher (person_id,contestproject_swjtu,contestproject_sichuan,contestproject_nation,customproject,master_course,techresearch_swjtu_project,techresearch_etc_newitem,techresearch_etc_olditem,techresearch_etc_module,techresearch_etc_course,techbook,paper_c,paper_issn,paper_noissn,mapcheck_count,course_director,project_director,master_platfom,misc_workscore,note) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)' ,[person_id,request.form[ 'contestproject_swjtu' ],request.form['contestproject_sichuan'],request.form['contestproject_nation'],request.form['customproject'],request.form['master_course'],request.form['techresearch_swjtu_project'],request.form['techresearch_etc_newitem'],request.form['techresearch_etc_olditem'],request.form['techresearch_etc_module'],request.form['techresearch_etc_course'],request.form['techbook'],request.form['paper_c'],request.form['paper_issn'],request.form['paper_noissn'],request.form['mapcheck_count'],request.form['course_director'],request.form['project_director'] ,request.form['master_platfom'] ,request.form['misc_workscore'],request.form['note']])
    db.commit()
    print("commit")
    flash('New  aftertech_teacher log was successfully inserted')
    return redirect(url_for('show_afterclass_teacher',person_id = person_id))

@app.route( '/person/<int:person_id>/afterclass_teacher/<int:id>/del' , methods=[ 'get' ])
def del_afterclass_teacher(person_id,id):
    #print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('DELETE from afterclass_teacher  where id = ?' ,(id,) )
    db.commit()
    print("commit")
    flash('A log was successfully DELETED')
    return redirect(url_for('show_afterclass_teacher',person_id=person_id))


@app.route( '/person/<int:person_id>/classtech_worker' )
def show_classtech_worker(person_id):
    db = get_db()
    cur = db.execute( 'select * from classtech_worker where person_id = ?',(person_id,) )
    items = cur.fetchall()
    return render_template( 'show_classtech_worker.html' , info={'items':items,'person_id':person_id})

@app.route( '/person/<int:person_id>/classtech_worker/add' , methods=[ 'POST' ])
def add_classtech_worker(person_id):
    #print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('insert into classtech_worker (person_id,basictech_days,systemtraining_days,contest_days,shortterm_days,totalwork_days,note) values (?,?,?,?,?,?,?)' ,[person_id,request.form[ 'basictech_days' ],request.form[ 'systemtraining_days' ],request.form[ 'contest_days' ],request.form['shortterm_days'],request.form['totalwork_days'],request.form['note']])
    db.commit()
    print("commit")
    flash('New classtech_worker log was successfully inserted')
    return redirect(url_for('show_classtech_worker',person_id = person_id))

@app.route( '/person/<int:person_id>/classtech_worker/<int:id>/del' , methods=[ 'get' ])
def del_classtech_worker(person_id,id):
    #print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('DELETE from classtech_worker  where id = ?' ,(id,) )
    db.commit()
    print("commit")
    flash('A log was successfully DELETED')
    return redirect(url_for('show_classtech_worker',person_id=person_id))


@app.route( '/person/<int:person_id>/afterclass_worker' )
def show_afterclass_worker(person_id):
    db = get_db()
    cur = db.execute( 'select * from afterclass_worker where person_id = ?',(person_id,) )
    items = cur.fetchall()
    return render_template( 'show_afterclass_worker.html' , info={'items':items,'person_id':person_id})

@app.route( '/person/<int:person_id>/afterclass_worker/add' , methods=[ 'POST' ])
def add_afterclass_worker(person_id):
    #print(request.form)
    #println('xxx')
    #print(request.form[ 'contestproject' ])
    #request.form[ 'techresearch_swjtu_project' ],request.form[ 'techresearch_etc_newitem' ],request.form['techresearch_etc_olditem'],request.form['techresearch_etc_module'],request.form['techresearch_etc_course'],request.form['techbook'],request.form['paper_c'],request.form['paper_issn'],request.form['paper_noissn'],request.form['making_nuetiac_days'],request.form['making_other_days'],request.form['note'];
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()

    db.execute('insert into afterclass_worker (person_id,contestproject,techresearch_swjtu_project,techresearch_etc_newitem,techresearch_etc_olditem,techresearch_etc_module,techresearch_etc_course,techbook,paper_c,paper_issn,paper_noissn,making_nuetiac_days,making_other_days,misc_workscore,note) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[person_id,request.form[ 'contestproject' ],request.form[ 'techresearch_swjtu_project' ],request.form[ 'techresearch_etc_newitem' ],request.form['techresearch_etc_olditem'],request.form['techresearch_etc_module'],request.form['techresearch_etc_course'],request.form['techbook'],request.form['paper_c'],request.form['paper_issn'],request.form['paper_noissn'],request.form['making_nuetiac_days'],request.form['making_other_days'],request.form['misc_workscore'],request.form['note']])
    db.commit()
    print("commit")
    flash('New classtech_worker log was successfully inserted')
    return redirect(url_for('show_afterclass_worker',person_id = person_id))


@app.route( '/person/<int:person_id>/afterclass_worker/<int:id>/del' , methods=[ 'get' ])
def del_afterclass_worker(person_id,id):
    #print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('DELETE from afterclass_worker  where id = ?' ,(id,) )
    db.commit()
    print("commit")
    flash('A log was successfully DELETED')
    return redirect(url_for('show_afterclass_worker',person_id=person_id))



@app.route( '/person/<int:person_id>/inno_days' )
def show_inno_days(person_id):
    db = get_db()
    cur = db.execute( 'select * from inno_days where person_id = ?',(person_id,) )
    items = cur.fetchall()
    return render_template( 'show_inno_days.html' , info={'items':items,'person_id':person_id})

@app.route( '/person/<int:person_id>/inno_days/add' , methods=[ 'POST' ])
def add_inno_days(person_id):
    print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('insert into inno_days (person_id,inno_days,note) values (?,?,?)' ,[person_id,request.form[ 'inno_days' ],request.form['note']])
    db.commit()
    print("commit")
    flash('New inno_days log was successfully inserted')
    return redirect(url_for('show_inno_days',person_id = person_id))


@app.route( '/person/<int:person_id>/inno_days/<int:id>/del' , methods=[ 'get' ])
def del_inno_days(person_id,id):
    #print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('DELETE from inno_days  where id = ?' ,(id,) )
    db.commit()
    print("commit")
    flash('A log was successfully DELETED')
    return redirect(url_for('show_inno_days',person_id=person_id))


@app.route( '/person/<int:person_id>/factors_teacher' )
def show_factors_teacher(person_id):
    db = get_db()
    cur = db.execute( 'select * from factors_teacher where person_id = ?',(person_id,) )
    items = cur.fetchall()
    return render_template( 'show_factors_teacher.html' , info={'items':items,'person_id':person_id})


@app.route( '/person/<int:person_id>/factors_teacher/add' , methods=[ 'POST' ])
def add_factors_teacher(person_id):
    print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('insert into factors_teacher (person_id,s_evaluation,s_environment,s_temperature,note) values (?,?,?,?,?)' ,[person_id,request.form[ 's_evaluation' ],request.form['s_environment'],request.form['s_temperature'],request.form['note']])
    db.commit()
    print("commit")
    flash('New factors_teacher log was successfully inserted')
    return redirect(url_for('show_factors_teacher',person_id = person_id))

@app.route( '/person/<int:person_id>/factors_teacher/<int:id>/del' , methods=[ 'get' ])
def del_factors_teacher(person_id,id):
    #print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('DELETE from factors_teacher  where id = ?' ,(id,) )
    db.commit()
    print("commit")
    flash('A log was successfully DELETED')
    return redirect(url_for('show_factors_teacher',person_id=person_id))



@app.route( '/person/<int:person_id>/factors_worker' )
def show_factors_worker(person_id):
    db = get_db()
    cur = db.execute( 'select * from factors_worker where person_id = ?',(person_id,) )
    items = cur.fetchall()
    return render_template( 'show_factors_worker.html' , info={'items':items,'person_id':person_id})


@app.route( '/person/<int:person_id>/factors_worker/add' , methods=[ 'POST' ])
def add_factors_worker(person_id):
    print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('insert into factors_worker (person_id,s_evaluation,s_environment,s_temperature,note) values (?,?,?,?,?)' ,[person_id,request.form[ 's_evaluation' ],request.form['s_environment'],request.form['s_temperature'],request.form['note']])
    db.commit()
    print("commit")
    flash('New factors_worker log was successfully inserted')
    return redirect(url_for('show_factors_worker',person_id = person_id))

@app.route( '/person/<int:person_id>/factors_worker/<int:id>/del' , methods=[ 'get' ])
def del_factors_worker(person_id,id):
    #print(request.form)
    if not session.get( 'logged_in' ):
        abort(401)
    db = get_db()
    db.execute('DELETE from factors_worker  where id = ?' ,(id,) )
    db.commit()
    print("commit")
    flash('A log was successfully DELETED')
    return redirect(url_for('show_factors_worker',person_id=person_id))



def calculate_achivement():
    return 1


@app.route( '/report/allwork' )
def report_allwork():
    db = get_db()
    cur = db.execute( 'select * from classtech_teacher')
    items_classtech_teacher = cur.fetchall()
    cur = db.execute( 'select * from classtech_worker')
    items_classtech_worker = cur.fetchall()
    cur = db.execute( 'select * from afterclass_teacher')
    items_afterclass_teacher = cur.fetchall()
    cur = db.execute( 'select * from afterclass_worker')
    items_afterclass_worker = cur.fetchall()

    cur = db.execute('''
        select * from person as p
        left join classtech_teacher as ct on p.id = ct.person_id
        left join afterclass_teacher as at on p.id = at.person_id
        left join inno_days as i on p.id = i.person_id
        left join factors_teacher as f on p.id = f.person_id
        where p.category = 'teacher'
     ''')
    items_teacher = cur.fetchall()

    cur = db.execute('''
        select * from person as p
        left join classtech_worker as cw on p.id = cw.person_id
        left join afterclass_worker as aw on p.id = aw.person_id
        left join inno_days as i on p.id = i.person_id
        left join factors_worker as f on p.id = f.person_id
        where p.category = 'worker'
     ''')
    items_worker = cur.fetchall()

    return render_template( 'report/allwork.html' , info = {'items_teacher':items_teacher,'items_worker':items_worker})

@app.route( '/person/<int:person_id>/report_mywork_teacher' )
def report_mywork_teacher(person_id):
    db = get_db()
    cur = db.execute('''
        select * from person as p
        left join classtech_teacher as cw on p.id = cw.person_id
        left join afterclass_teacher as aw on p.id = aw.person_id
        left join inno_days as i on p.id = i.person_id
        left join factors_teacher as f on p.id = f.person_id
        where p.category = 'teacher' and p.id = ?
     ''',(person_id,))
    items = cur.fetchall()
    info = {}
    info['person_id'] = person_id;
    if(len(items) > 0 ):
        item = items[0]
        S_evaluation = item['s_evaluation']
        S_environment = item['s_environment']
        S_temperature = item['s_temperature']
        #CLASS TEACH
        info['G_systemtraining_machanical'] = 1.0*item['systemtraining_machanical_days']*item['systemtraining_machanical_stucount']/120/24
        info['G_systemtraining_other'] = item['systemtraining_other_days']*0.005
        info['G_compulsorycourse'] = item['compulsorycourse_techhour']*item['compulsorycourse_factor']*item['compulsorycourse_stucount']/208/80.0
        if(item['elective_isnew'] == 0):
            info['G_elective'] =item['elective_techhour']*item['elective_stucount']*0.8/208/80
        else:
            info['G_elective'] =item['elective_techhour']*item['elective_stucount']*1.05/208/80
        info['G_graduationproject'] = item['graduationproject_stucount']/20.0
        info['G_nuetiac'] = item['nuetiac_sichuan']*0.04+item['nuetiac_nation']*0.16+(item['nuetiac_plan']*0.5+item['nuetiac_make']*0.3+item['nuetiac_swjtu']*0.2)*0.02
        info['G_make'] = item['make_techdays']*0.005
        info['G_classtech'] =(item['basictech_days']+item['shortterm_days']*S_temperature)*S_environment/item['totalwork_days']+info['G_systemtraining_machanical']+info['G_systemtraining_other']+info['G_compulsorycourse']+info['G_elective']+info['G_graduationproject']+info['G_nuetiac']+info['G_make']
        #AFTER CLASS
        info['G_contestproject'] =item['contestproject_swjtu']*0.03+item['contestproject_sichuan']*0.05+item['contestproject_nation']*0.1+item['customproject']*0.03
        info['G_techresearch_etc'] = item['techresearch_etc_newitem']+item['techresearch_etc_olditem']+item['techresearch_etc_module']+item['techresearch_etc_course']
        info['G_paper'] = item['paper_c']*0.1+item['paper_issn']*0.03+item['paper_noissn']*0.01
        info['G_mapcheck'] =item['mapcheck_count']*0.002
        info['G_teach_direct'] = item['course_director']*0.15+item['project_director']*0.15+item['master_platfom']*0.15
        info['G_misc_workscore'] =item['misc_workscore']*abs(1-info['G_classtech'])*0.2
        info['G_afterclass'] =info['G_contestproject']+item['master_course']+item['techresearch_swjtu_project']+info['G_techresearch_etc']+item['techbook']+info['G_paper']+info['G_mapcheck']+info['G_teach_direct']+info['G_misc_workscore']
        #INNOVATION
        info['I'] = item['inno_days']*0.005
        print info

    #print I
    return render_template( 'report/mywork.html' , info = info)

@app.route( '/person/<int:person_id>/report_mywork_worker' )
def report_mywork_worker(person_id):
    db = get_db()
    cur = db.execute('''
        select * from person as p
        left join classtech_worker as cw on p.id = cw.person_id
        left join afterclass_worker as aw on p.id = aw.person_id
        left join inno_days as i on p.id = i.person_id
        left join factors_worker as f on p.id = f.person_id
        where p.category = 'worker' and p.id = ?
     ''',[person_id])

    items = cur.fetchall()
    #print items
    item = items[0]
    S_evaluation = item['s_evaluation']
    S_environment = item['s_environment']
    S_temperature = item['s_temperature']
    info = {}
    info['person_id'] = person_id;

    #CLASS TEACH
    info['G_classtech'] =(item['basictech_days']+item['shortterm_days']*S_temperature+item['systemtraining_days']+item['contest_days'])*S_environment/item['totalwork_days']
    #AFTER CLASS
    info['G_contestproject']=item['contestproject']*0.005
    info['G_techresearch_etc']= item['techresearch_etc_newitem']*1.0+item['techresearch_etc_olditem']*1.0+item['techresearch_etc_module']*1.0+item['techresearch_etc_course']*1.0

    info['G_paper'] = item['paper_c']*0.1+item['paper_issn']*0.03+item['paper_noissn']*0.01
    info['G_nuetiac_make'] =item['making_nuetiac_days']*0.005
    info['G_other_make'] = item['making_other_days']*0.005/7
    info['G_misc_workscore'] =item['misc_workscore']*(1-info['G_classtech'])*0.8
    info['G_afterclass'] =info['G_contestproject']+item['techresearch_swjtu_project']*1.0+info['G_techresearch_etc']+item['techbook']+info['G_paper']+info['G_nuetiac_make']+info['G_other_make']+info['G_misc_workscore']
    #INNOVATION
    info['I'] = item['inno_days']*0.005
    print item
    print info
    return render_template( 'report/mywork.html' , info=info)



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
            return redirect(url_for('show_persons'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
