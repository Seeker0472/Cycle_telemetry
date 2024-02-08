from flask import jsonify


def success(data=None, msg=None):
    if data is None:
        data = {}
    if msg is None:
        msg = {}
    return jsonify({
        'stat': "OK",
        'data': data,
        'msg': msg
    })


def fail(msg=None):
    if msg is None:
        msg = {}
    return jsonify({
        'stat': "ERROR",
        'msg': msg
    })
