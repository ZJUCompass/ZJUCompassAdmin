# -*- coding:utf-8 -*-
# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")
import json
import datetime
import dump_csv

# configuration
DATABASE = 'data/zjucompass.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    g.db.close()

@app.route('/')
@app.route('/teachers')
def show_entries():
    cur = g.db.execute('select * from teacher_info where department="计算机科学与技术学院"')
    entries = [dict(teacher_id=row[0], name=row[1], department=row[2], title=row[3], phone=row[4], email=row[5], building=row[6], room=row[7], field=row[8]) for row in cur.fetchall()]
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('show_entries.html', type="teacher", entries=entries)


@app.route('/feedback')
def show_feedback():
    cur = g.db.execute('select * from feedback order by timestamp desc')
    entries = [dict(timestamp=row[0], feedback=row[1], email=row[2], phone=row[3]) for row in cur.fetchall()]
    print len(entries)
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('show_feedback.html', type="feedback", entries=entries)



@app.route('/correct')
def show_correct():
    cur = g.db.execute('select * from correct_teacher order by timestamp desc')
    entries = [dict(teacher_id=row[1], timestamp=row[2], name=row[3], department=row[4], title=row[5], phone=row[6], email=row[7], building=row[8], room=row[9], field=row[10]) for row in cur.fetchall()]
    print len(entries)
    print "Hello World"
    for entry in entries:
        print entry
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('show_correct.html', type="correct", entries=entries)


@app.route('/matters')
def show_matters():
    cur = g.db.execute('select matter_id,matter_name,matter_meterial,matter_description,matter_time,matter_consult_phone,matter_address,matter_detail_url from matter_info;')
    entries = [dict(matter_id=row[0], matter_name=row[1], matter_meterial=row[2], matter_description=row[3], matter_time=row[4], matter_consult_phone=row[5], matter_address=row[6], matter_detail_url=row[7]) for row in cur.fetchall()]
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('show_matters.html', type="matter", entries=entries)

@app.route('/api/download_teacher',methods=['GET'])
def download_teacher():
    dump_csv.dump_info("static/teachers.csv","teacher")
    return redirect("/static/teachers.csv")

@app.route('/api/download_matter',methods=['GET'])
def download_matter():
    dump_csv.dump_info("static/matters.csv","teacher")
    return redirect("/static/matters.csv")



@app.route('/api/feedback',methods=['POST'])
def get_feedback():
    jsonStr = request.data
    print type(jsonStr)
    print jsonStr
    print jsonStr.decode("utf-8")
    data = json.loads(jsonStr)
    feedback = data['feedback']
    email = data['email']
    phone = data['phone']

    print feedback
    print email
    print phone

    currTime = datetime.datetime.now()
    timeStr = currTime.strftime("%Y-%m-%d %H:%M:%S")
    print timeStr
    
    sqlcmd = "insert into feedback(timestamp, feedback, email, phone) values('%s','%s','%s','%s')"%(timeStr, feedback, email, phone)
    g.db.execute(sqlcmd)
    g.db.commit()

    return '{"code":200}'

@app.route('/api/correct_teacher',methods=['POST'])
def get_correct_teacher():
    jsonStr = request.data
    data = json.loads(jsonStr)
    print data 
    currTime = datetime.datetime.now()
    timeStr = currTime.strftime("%Y-%m-%d %H:%M:%S")
    sqlcmd = "insert into correct_teacher(timestamp,teacher_id,name,email,phone,title,room,field,department) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(timeStr,data['id'],data['name'],data['email'],data['phone'],data['title'],data['location'],data['research'],data['dept'])
    g.db.execute(sqlcmd)
    g.db.commit()

    return '{"code":200}'

@app.route('/api/check_update',methods=['POST','GET'])
def get_version():
    return "1.0.0"

@app.route('/add', methods=['GET','POST'])
def add_entry():
    if request.method == 'GET':
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return render_template('add_entry.html')
    else:
        name = request.form['name']
        department = request.form['department']
        title = request.form['title']
        phone = request.form['phone']
        email = request.form['email']
        building = request.form['building']
        room = request.form['room']
        field = request.form['field']
        
        sqlcmd = "insert into teacher_info (name, department, title, phone, email, building, room, field) values('%s','%s','%s','%s','%s','%s','%s','%s')" % (name,department,title,phone,email,building,room,field)
        g.db.execute(sqlcmd)
        g.db.commit()
        flash('The new entry was added')
        return redirect(url_for('show_entries'))

    
@app.route('/add_matter', methods=['GET','POST'])
def add_matter():
    if request.method == 'GET':
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return render_template('add_matter.html')
    else:
        name = request.form['name']
        m_id = request.form['id']
        meterial = request.form['meterial']
        description = request.form['description']
        time = request.form['time']
        address = request.form['address']
        consult_phone = request.form['consult_phone']
        detail_url = request.form['detail_url']
        
        sqlcmd = "insert into matter_info (matter_id, matter_name, matter_meterial, matter_description, matter_time, matter_address, matter_consult_phone, matter_detail_url) values('%s','%s','%s','%s','%s','%s','%s','%s')" % (m_id, name, meterial, description, time, address, consult_phone, detail_url)
        g.db.execute(sqlcmd)
        g.db.commit()
        flash('The new matter was added')
        return redirect(url_for('show_matters'))

@app.route('/del',methods=['GET'])
def del_entry():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    teacher_id = request.args.get('id','-1')
    if teacher_id == "-1":
        flash("Bad teacher_id!")
        return redirect(url_for('show_entries'))
     
    sqlcmd = "delete from teacher_info where teacher_id='%s'" % (teacher_id)
    g.db.execute(sqlcmd)
    g.db.commit()
    flash('This entry was successfully deleted')
    return redirect(url_for('show_entries'))


@app.route('/del_matter',methods=['GET'])
def del_matter():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    matter_id = request.args.get('matter_id','-1')
    if matter_id == "-1":
        flash("Bad teacher_id!")
        return redirect(url_for('show_matters'))
     
    sqlcmd = "delete from matter_info where matter_id='%s'" % (matter_id)
    g.db.execute(sqlcmd)
    g.db.commit()
    flash('This matter was successfully deleted')
    return redirect(url_for('show_matters'))

@app.route('/edit', methods=['GET','POST'])
def edit_entry():
    if request.method == 'POST':
        teacher_id = request.form['teacher_id']
        name = request.form['name']
        department = request.form['department']
        title = request.form['title']
        phone = request.form['phone']
        email = request.form['email']
        building = request.form['building']
        room = request.form['room']
        field = request.form['field']
        
        sqlcmd = "update teacher_info set name='%s',department='%s',title='%s',phone='%s',email='%s',building='%s',room='%s',field='%s' where teacher_id='%s'" % (name,department,title,phone,email,building,room,field,teacher_id)
        g.db.execute(sqlcmd)
        g.db.commit()
        flash('This entry was successfully updated')
        return redirect(url_for('show_entries'))

    else:
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        
        teacher_id = request.args.get('id','-1')
        if teacher_id == "-1":
            flash("Bad teacher_id!")
            return redirect(url_for('show_entries'))
        cur = g.db.execute('select * from teacher_info where teacher_id = "%s"'%teacher_id)
        #print cur.fetchall()[0]
        results = cur.fetchall()
        if not results:
            flash("This teacher_id does not exist!")
            return redirect(url_for('show_entries'))
        row = results[0]
        entry = dict(teacher_id=row[0], name=row[1], department=row[2], title=row[3], phone=row[4], email=row[5], building=row[6], room=row[7], field=row[8])
        return render_template('edit_entry.html', entry=entry)
        #entrieds = [dict(teacher_id=row[0], name=row[1], department=row[2], title=row[3], phone=row[4], email=row[5], building=row[6], room=row[7], field=row[8]) for row in cur.fetchall()]


@app.route('/edit_matter', methods=['GET','POST'])
def edit_matter():
    if request.method == 'POST':
        matter_id = request.form['id']
        matter_name = request.form['name']
        matter_meterial = request.form['meterial']
        matter_description = request.form['description']
        matter_time = request.form['time']
        matter_address = request.form['address']
        matter_consult_phone = request.form['consult_phone']
        matter_detail_url = request.form['detail_url']
        
        sqlcmd = "update matter_info set matter_name='%s',matter_meterial='%s',matter_description='%s',matter_time='%s',matter_address='%s',matter_consult_phone='%s',matter_detail_url='%s' where matter_id='%s'" % (matter_name,matter_meterial,matter_description,matter_time,matter_address,matter_consult_phone,matter_detail_url,matter_id)
        print sqlcmd
        g.db.execute(sqlcmd)
        g.db.commit()
        flash('This matter was successfully updated')
        return redirect(url_for('show_matters'))

    else:
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        
        matter_id = request.args.get('id','-1')
        if matter_id == "-1":
            flash("Bad teacher_id!")
            return redirect(url_for('show_matters'))
        cur = g.db.execute('select matter_name,matter_id,matter_meterial,matter_description,matter_time,matter_address,matter_consult_phone,matter_detail_url from matter_info where matter_id = "%s"'%matter_id)
        #print cur.fetchall()[0]
        results = cur.fetchall()
        if not results:
            flash("This matter_id does not exist!")
            return redirect(url_for('show_matters'))
        row = results[0]
        entry = dict(matter_name=row[0], matter_id=row[1], matter_meterial=row[2], matter_description=row[3], matter_time=row[4], matter_address=row[5], matter_consult_phone=row[6], matter_detail_url=row[7])
        return render_template('edit_matter.html', entry=entry)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
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

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
