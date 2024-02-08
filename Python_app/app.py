from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from db import get_info_db, add_info_db
import response
import Service.mp4_gpx_extractor as mp4_gpx_extractor
import Service.fitphaser as fit_phaser

app = Flask(__name__)


@app.route('/')
@cross_origin()
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/api/getAllCut', methods=['GET', 'POST'])
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


@app.route('/api/getFileList', methods=['GET', 'POST'])
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


#
# @app.route('/test/<int:test>')
# def te(test):
#     return "input" + test
#
#
# @app.route('/test/args')
# def getarg():
#     # page=request.args.get("Key", default=1, type=int);
#     # return f"arg="+page
#     page = request.args.get("Key", default=1, type=int)
#     return f"arg={page}"


if __name__ == '__main__':
    app.debug = True
    app.run()
