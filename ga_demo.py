import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import json
from utils import archer_details

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'ga_demo.db'),
    DEBUG=True,
    SECRET_KEY='development key'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#GLOBAL VARIABLES

#loaded from db at start and when db changes
archer_list = []  # list format for easy html passing
id_to_archer_details = {}
loaded_member_details = False

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    #rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Called for testing
def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def load_members_from_db(needs_reload=False):
    global archer_list
    global id_to_archer_details
    # we've already loaded archers and don't think anything has changed
    if archer_list != [] and not needs_reload:
        return
    db = get_db()
    cur = db.execute("""select id,
                        firstname,
                        lastname,
                        byear,
                        gender
                        from members order by firstname""")
    archer_list = cur.fetchall()
    id_to_archer_details = {}
    for archer in archer_list:
        id_to_archer_details[archer[0]] = archer_details(archer)

def load_member_details_from_db():
    global id_to_archer_details
    global loaded_member_details
    # we've already loaded details and don't think anything has changed
    db = get_db()
    # grab the most recent entry for each archer
    cur = db.execute("""select id,
                        MAX(date),
                        discipline,
                        owns_equipment,
                        draw_weight,
                        draw_length,
                        equipment_description,
                        distance,
                        joad_day
                        from member_details group by id""")
    row_details = cur.fetchall()
    for row in row_details:
        archer_detail = id_to_archer_details.get(row[0], None)
        assert archer_detail is not None
        archer_detail.set_details(row)
        id_to_archer_details[row[0]] = archer_detail

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def landing():
    # TODO read at start up
    load_members_from_db()
    load_member_details_from_db()
    return render_template('home.html', archer_list=archer_list)

# add a new archer to the joad program
@app.route('/add_archer', methods=['GET', 'POST'])
def add_archer():
    if request.method == 'GET':
        return render_template('add_archer.html')
    else:
        query = """insert into members (firstname, lastname, gender, byear)
            values (?, ?, ?, ?)"""
        flash_msg = 'New archer was successfully added'
        db = get_db()
        db.execute(query, (request.form['firstname'],
                           request.form['lastname'],
                           request.form['gender'],
                           request.form['byear']))
        db.commit()
        flash(flash_msg)
        # after we add a new archer, grab new one from db
        needs_reload = True
        load_members_from_db(needs_reload)
        return redirect(url_for('landing'))

# edit the basic info for selected archer
@app.route('/edit_details', methods=['GET', 'POST'])
def edit_details():
    if request.method == 'GET':
        archer_details = id_to_archer_details.get(
            int(request.args.get('name_selecter')), None)
        assert archer_details is not None
        return render_template('edit_details.html', archer_dict=archer_details.__dict__)
    else:
        query = """insert into member_details (id,
                                               discipline,
                                               owns_equipment,
                                               draw_weight,
                                               draw_length,
                                               equipment_description,
                                               distance,
                                               joad_day)
                   values (?, ?, ?, ?, ?, ?, ?, ?)"""
        flash_msg = 'New data was successfully added'
        db = get_db()
        if ('owns_equipment' in request.form):
            owns_equipment = "1"
        else:
            owns_equipment = "0"
        db.execute(query, (request.form['id'],
                           request.form['discipline'],
                           owns_equipment,
                           request.form['draw_weight'],
                           request.form['draw_length'],
                           request.form['equipment_description'],
                           request.form['distance_selecter'],
                           request.form['day_selecter']))
        db.commit()
        flash(flash_msg)
        return redirect(url_for('landing'))

@app.route('/review', methods=['GET', 'POST'])
def review():
    return redirect(url_for('landing'))


if __name__ == "__main__":
    app.run(debug=True)
