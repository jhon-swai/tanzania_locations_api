# all the imports
import sqlite3
import os 
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

from flask_cors import CORS

# path to database 
basedir = os.path.abspath(os.path.dirname(__file__))

# configuration
DATABASE = os.path.join(basedir, 'location.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)



def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def show_entries():
    regions = ['arusha', 'daressalaam', 'dodoma', 'geita', 'iringa', 'kagera', 'katavi', 'kigoma', 'kilimanjaro', 'lindi', 'manyara', 'mara', 'mbeya', 'morogoro', 'mtwara', 'mwanza', 'njombe', 'pwani', 'rukwa', 'ruvuma', 'shinyanga', 'simiyu', 'singida', 'singida', 'songwe', 'tabora']
    
    return render_template('show_entries.html', entries=regions)


# Get all districts in a region
@app.route('/districts/<region_name>', methods=['GET','POST'])
def show_district(region_name):
    regions = ['arusha', 'daressalaam', 'dodoma', 'geita', 'iringa', 'kagera', 'katavi', 'kigoma', 'kilimanjaro', 'lindi', 'manyara', 'mara', 'mbeya', 'morogoro', 'mtwara', 'mwanza', 'njombe', 'pwani', 'rukwa', 'ruvuma', 'shinyanga', 'simiyu', 'singida', 'singida', 'songwe', 'tabora']
    
    if region_name in regions:
        ind = regions.index(region_name)
        region = regions[ind]
        sql_code = 'select distinct district from ' + region
        cur = g.db.execute(sql_code)
        districts = [ row[0] for row in cur.fetchall()]

    else:
        districts = ['not found']


    data = districts


    data_dict = {}
    num = 0
    for val in data:
        data_dict[num]=val
        num+=1

    return jsonify(data_dict)


# all wards in a region
@app.route('/wards/<region_name>', methods=['GET', 'POST'])
def show_all_wards(region_name):
    regions = ['arusha', 'daressalaam', 'dodoma', 'geita', 'iringa', 'kagera', 'katavi', 'kigoma', 'kilimanjaro', 'lindi', 'manyara', 'mara', 'mbeya', 'morogoro', 'mtwara', 'mwanza', 'njombe', 'pwani', 'rukwa', 'ruvuma', 'shinyanga', 'simiyu', 'singida', 'singida', 'songwe', 'tabora']
    
    # convert the region to lowercase 
    if not region_name.islower(): 
        region_name = region_name.lower()
    
    # check if the region exists 
    if region_name in regions:
        ind = regions.index(region_name)
        region = regions[ind]
        sql_code = 'select distinct ward from ' + region
        
        cur = g.db.execute(sql_code)
        
        wards = [ row[0] for row in cur.fetchall()]
        data = wards 
    else:
        # This returns that the region was not found and the ward and district not checked
        data = ['region not found']
    
    data_dict = {}
    num = 0
    for val in data:
        data_dict[num]=val
        num+=1

    return jsonify(data_dict)

# wards in a specific district
@app.route('/wards/<region_name>/<district_name>/', methods=['GET', 'POST'])
def show_wards(region_name,district_name):
    regions = ['arusha', 'daressalaam', 'dodoma', 'geita', 'iringa', 'kagera', 'katavi', 'kigoma', 'kilimanjaro', 'lindi', 'manyara', 'mara', 'mbeya', 'morogoro', 'mtwara', 'mwanza', 'njombe', 'pwani', 'rukwa', 'ruvuma', 'shinyanga', 'simiyu', 'singida', 'singida', 'songwe', 'tabora']
    
    # convert the region to lowercase 
    if not region_name.islower(): 
        region_name = region_name.lower()
    
    # check if the region exists 
    if region_name in regions:
        ind = regions.index(region_name)
        region = regions[ind]
        sql_code = 'select distinct district from ' + region
        
        cur = g.db.execute(sql_code)
        
        districts = [ row[0] for row in cur.fetchall()]

        # Checking if the disctrict input is a lower case or upper
        if not district_name.isupper():
            district_name = district_name.upper()

        if district_name in districts:
            ind = districts.index(district_name)
            district = districts[ind]
            # where the district = district
            sql_code = 'select distinct ward from ' + region + ' where district = ?'
            cur = g.db.execute(sql_code, [district])
            wards = [ row[0] for row in cur.fetchall()]

            # assign the data 
            data = wards
        
        else:
            data = ['ward not found']
    else:
        # This returns that the region was not found and the ward and district not checked
        data = ['region not found']
    
    data_dict = {}
    num = 0
    for val in data:
        data_dict[num]=val
        num+=1

    return jsonify(data_dict)

# all streets in a ward 
@app.route('/streets/<region_name>/<district_name>/<ward_name>', methods=['GET', 'POST'])
def show_streets(region_name, district_name, ward_name):
    regions = ['arusha', 'daressalaam', 'dodoma', 'geita', 'iringa', 'kagera', 'katavi', 'kigoma', 'kilimanjaro', 'lindi', 'manyara', 'mara', 'mbeya', 'morogoro', 'mtwara', 'mwanza', 'njombe', 'pwani', 'rukwa', 'ruvuma', 'shinyanga', 'simiyu', 'singida', 'singida', 'songwe', 'tabora']
    
    # convert the region to lowercase 
    if not region_name.islower(): 
        region_name = region_name.lower()
    
    # check if the region exists 
    if region_name in regions:
        ind = regions.index(region_name)
        region = regions[ind]
        sql_code = 'select distinct district from ' + region
        
        cur = g.db.execute(sql_code)
        
        districts = [ row[0] for row in cur.fetchall()]

        # Checking if the disctrict input is a lower case or upper
        if not district_name.isupper():
            district_name = district_name.upper()

        if district_name in districts:
            ind = districts.index(district_name)
            district = districts[ind]
            # where the district = district
            sql_code = 'select distinct ward from ' + region + ' where district = ?'
            cur = g.db.execute(sql_code, [district])
            wards = [ row[0] for row in cur.fetchall()]

            if not ward_name.isupper():
                ward_name = ward_name.upper()

            if ward_name in wards:
                ind = wards.index(ward_name)
                ward = wards[ind]
                sql_code = "SELECT DISTINCT street from " + region + ' where district = ? and ward = ?'
                cur = g.db.execute(sql_code, [district, ward])
                streets  = [ row[0] for row in cur.fetchall()]

                data = streets
        
        else:
            data = ['ward not found']
    else:
        # This returns that the region was not found and the ward and district not checked
        data = ['region not found']
    
    data_dict = {}
    num = 0
    for val in data:
        data_dict[num]=val
        num+=1

    return jsonify(data_dict)


# Error handling 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()