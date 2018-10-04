import json
import time

# Need to be installed
import flask
from flask import Flask, request
from flaskext.mysql import MySQL
from gripcontrol import GripPubControl
import redis

app = Flask(__name__)

cache = redis.StrictRedis(host='redis', port=6379, charset="utf-8", decode_responses=True)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Verkada123'
app.config['MYSQL_DATABASE_DB'] = 'camera'
app.config['MYSQL_DATABASE_HOST'] = 'db' 
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

@app.route('/logs', methods=['GET'])
def logs():
    camera_id = request.args.get('cam')
    # pushpin private control
    pub = GripPubControl({'control_uri': 'http://proxy:5561'})
    pub.publish_http_response(camera_id + '_channel',
                              '{"event": "USER_REQUESTED"}')
    # wait receive_log() to finish updating current_log
    # FIXME: This part need be optimized
    time.sleep(0.4)
    return json.dumps(cache.get('current_log')), 200, {'ContentType': 'application/json'}

@app.route('/check_user_request', methods=['GET'])
def check_user_request():
    camera_id = request.args.get('cam')
    response = flask.Response('{"event": "POLLING_RENEWED"}')
    response.headers['Content-Type'] = 'application/json'
    response.headers['Grip-Hold'] = 'response'  # long-polling
    response.headers['Grip-Channel'] = camera_id + '_channel'  # make client subscribe to this channel
    return response

@app.route('/receive_log', methods=['POST'])
def receive_log():
    cursor = mysql.connect().cursor() 
    cursor.execute("CREATE TABLE IF NOT EXISTS logs(timestamp_camera VARCHAR(30) PRIMARY KEY, recordtime VARCHAR(20), camera VARCHAR(10), event VARCHAR(100));")
    # update current_log
    current_log = request.form.to_dict()
    cache.set('current_log', current_log)
    # add to db
    camera_id = request.args.get('cam')
    cursor = mysql.connect().cursor() 
    for log_record_timestamp in current_log:
        cursor.execute("INSERT IGNORE INTO logs(timestamp_camera, recordtime, camera, event) VALUES ('" + log_record_timestamp + " - " + camera_id + "', '"
                  + log_record_timestamp + "', '"
                  + camera_id + "', '" + current_log[log_record_timestamp] + "' );")

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    


