from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'playersData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'players Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblplayersImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, players=result)


@app.route('/view/<int:player_id>', methods=['GET'])
def record_view(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblplayersImport WHERE id=%s', player_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', player=result[0])


@app.route('/edit/<int:player_id>', methods=['GET'])
def form_edit_get(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblplayersImport WHERE id=%s', player_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', player=result[0])


@app.route('/edit/<int:player_id>', methods=['POST'])
def form_update_post(player_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldTeam'), request.form.get('fldPosition'),
                 request.form.get('fldHeight'), request.form.get('fldWeight'),
                 request.form.get('fldAge'), player_id)
    sql_update_query = """UPDATE tblplayersImport t SET t.fldName = %s, t.fldTeam = %s, t.fldPosition = %s, t.fldHeight 
    = %s, t.fldWeight = %s, t.fldAge = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/players/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New player Form')


@app.route('/players/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldTeam'), request.form.get('fldPosition'),
                 request.form.get('fldHeight'), request.form.get('fldWeight'),
                 request.form.get('fldAge'))
    sql_insert_query = """INSERT INTO tblplayersImport (fldName,fldTeam,fldPosition,fldHeight,fldWeight,fldAge) 
    VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:player_id>', methods=['POST'])
def form_delete_post(player_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblplayersImport WHERE id = %s """
    cursor.execute(sql_delete_query, player_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/players', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblplayersImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/players/<int:player_id>', methods=['GET'])
def api_retrieve(player_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblplayersImport WHERE id=%s', player_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/players/<int:player_id>', methods=['PUT'])
def api_edit(player_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['fldName'], content['fldTeam'], content['fldPosition'],
                 content['fldHeight'], content['fldWeight'],
                 content['fldAge'],player_id)
    sql_update_query = """UPDATE tblplayersImport t SET t.fldName = %s, t.fldTeam = %s, t.fldPosition = %s, t.fldHeight = 
        %s, t.fldWeight = %s, t.fldAge = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/players', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['fldName'], content['fldTeam'], content['fldPosition'],
                 content['fldHeight'], content['fldWeight'],
                 content['fldAge'])
    sql_insert_query = """INSERT INTO tblplayersImport (fldName,fldTeam,fldPosition,fldHeight,fldWeight,fldAge) 
    VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/players/<int:player_id>', methods=['DELETE'])
def api_delete(player_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblplayersImport WHERE id = %s """
    cursor.execute(sql_delete_query, player_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
