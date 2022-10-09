import json, sys, argparse, os
import flask
from flask import jsonify

parser = argparse.ArgumentParser()
parser.add_argument('--path1', '--1', nargs=1, type=str, help='file name of the prediction of the receipts recognition')
folders = vars(parser.parse_args())
path1 = folders['path1'][0]

with open(path1, mode='r',encoding='utf-8') as report_json:
    globals()['ReportJson'] = json.load(report_json)

app = flask.Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route('/', methods=['GET'])
def home():
    return jsonify(ReportJson)

app.run()