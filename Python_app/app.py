import json

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from db import get_info_db, add_info_db
import response
import Service.mp4_gpx_extractor as mp4_gpx_extractor
import Service.fitphaser as fit_phaser
import Service.xingzhe as xingzhe
from flask_socketio import SocketIO, emit
import db.Project_page_db as Project_page_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
@cross_origin()
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/api/getAllCut', methods=['POST'])
@cross_origin()
def get_all_cut():
    if request.is_json:
        try:
            data = request.get_json()
            res = get_info_db.all_cut_info(data)
        except Exception as e:
            return response.fail(str(e))
        return response.success(res)
    return response.fail('Bad Request')


@app.route('/api/getFileList', methods=['POST'])
@cross_origin()
def get_all_file_info():
    if request.is_json:
        try:
            data = request.get_json()
            res = get_info_db.get_all_file(data)
        except Exception as e:
            return response.fail(str(e))
        return response.success(res)
    return response.fail('Bad Request')


@app.route('/api/addCut', methods=['POST'])
@cross_origin()
def add_cut():
    if request.is_json:
        try:
            data = request.get_json()
            name = data.get('name')
            comments = data.get('description')
            cut_id = add_info_db.add_cut(name, comments)
            return response.success({
                "id": cut_id
            })
        except Exception as e:
            return response.fail(str(e))
    return response.fail("Bad Request")


@app.route('/api/addFile', methods=['POST'])
@cross_origin()
def add_file():
    ret = ""
    if request.is_json:
        try:
            data = request.get_json()
            name = data.get('name')
            comments = data.get('description')
            file_type = data.get('type')
            path = data.get('path')

            match file_type:
                case 'MP4':
                    ret = mp4_gpx_extractor.extract_mp4(path, name, comments)
                case 'FIT':
                    ret = fit_phaser.phase_fit(path, name, comments)
                case 'GPX':
                    ret = mp4_gpx_extractor.read_gpx(path, name, comments)
                case 'CSV':
                    raise Exception("CSV not supported yet")
                case _:
                    raise Exception(f"Unsupported file type: {file_type}")
        except Exception as e:
            return response.fail(str(e))

    return response.success({'id': ret})


@app.route('/api/addAccount', methods=['POST'])
@cross_origin()
def add_account():
    if request.is_json:
        try:
            data = request.get_json()
            platform = data.get('Platform')
            account = data.get('account')
            password = data.get('passWord')
            if platform == 1:
                xingzhe.login(account, password)
                return response.success()
            else:
                raise Exception("Unsupported platform")
        except Exception as e:
            return response.fail(str(e))
    return response.fail("Bad Request")


@app.route('/api/addFilesToTimeLine', methods=['POST'])
@cross_origin()
def add_files_to_timeline():
    if request.is_json:
        try:
            data = request.get_json()
            time_line_id = data.get('TimeLineID')
            file_ids = data.get('file_ids')
            cut_id = data.get('cut_id')
            print(time_line_id, file_ids, cut_id)
            add_info_db.add_segments(cut_id, time_line_id, file_ids)
            return response.success()
        except Exception as e:
            return response.fail(str(e))
    return response.fail("Bad Request")


@socketio.on('message', namespace='/test')
def handle_message(data):
    print('received message: ' + data)
    return "Success"


@socketio.on('get_all_data', namespace='/test')
def handle_get_all(data):
    print(data.get("cutid"))
    result=Project_page_db.get_all_info(data.get("cutid"))
    emit('reset_all', json.dumps(result))


if __name__ == '__main__':
    socketio.run(app)
