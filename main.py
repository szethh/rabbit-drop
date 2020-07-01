from flask import Flask, Response, redirect, render_template, request, url_for, send_file
from tinydb import TinyDB, Query
from datetime import datetime
import os, json, argparse, random

def save_file(file, user='anon'): # get user from cookies or login
    name, ext = os.path.splitext(file.filename)
    guid = str(int(random.random()*1000)) # get unique guid
    date = datetime.now().astimezone().replace(microsecond=0).isoformat()
    print('\n\n\n', date, '\n\n\n')
    new_name = guid + ext
    destination = "/".join([UPLOAD_DIR, new_name])
    file.save(destination)
    db.insert({'name': name, 'ext': ext, 'destination': destination,
           'id': guid, 'details': {'user': user, 'date': date}})
    print(date + ':', user, 'uploaded', name + ext, 'with id', guid)
    return guid

db = TinyDB('db.json')
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(APP_ROOT, 'uploads')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/file/<file_id>')
def view_file(file_id):
    file = db.get(Query().id == file_id)
    if file == None:
        return page_not_found(404)
    return render_template("file.html", data=file)

@app.route('/file/<file_id>/dl')
def download_file(file_id):
    file = db.get(Query().id == file_id)
    if file == None:
        return page_not_found(404)
    path, name = file['destination'], file['name'] + file['ext']
    print(path, name)
    return send_file(path, attachment_filename=name, as_attachment=True)

@app.route('/file-upload', methods=['POST'])
def upload_file():
    ids = []
    print(len(request.files.getlist('file')))
    for file in request.files.getlist("file"):
        ids.append(save_file(file))
    if len(ids) == 0: return ''
    print('redirecting', ids[0])
    return url_for('view_file', file_id=ids[0])

@app.route('/purge')
def purge_db():
    db.truncate()
    for f in os.listdir(UPLOAD_DIR):
        os.remove(os.path.join(UPLOAD_DIR, f))
    return str(len(db)) + ' | ' + str(len(os.listdir(UPLOAD_DIR)))

if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
        help="ip address of the device")
    ap.add_argument("-p", "--port", type=int, required=True,
        help="ephemeral port number of the server (1024 to 65535)")
    args = vars(ap.parse_args())

    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True)
