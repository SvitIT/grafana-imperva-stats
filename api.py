import os
from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename
from log_helper import timeSplit
import zipfile


app = Flask(__name__)


UPLOAD_FOLDER = './stats'
ALLOWED_EXTENSIONS = {'csv', 'zip'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')

            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            # print('wrong filename')

            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print('saved')

            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            timeSplit(open(os.path.join(UPLOAD_FOLDER, filename)))
            # return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route("/upload_zip/<measurement>", methods=['GET', 'POST'])
def upload_zip_file_measurement(measurement):
    flash('upload_zip triggered!')
    if request.method == 'POST':
        # check if the post request has the file part
        # print('post')
        if 'file' not in request.files:
            flash('No file part')
            # print('no file')

            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            # print('wrong filename')

            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # print('saved')

            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(UPLOAD_FOLDER)
            path = path[:-4]
            # print('running data processing for {} file'.format(path))
            timeSplit(open(path), measurement)
            # return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route("/upload_zip", methods=['GET', 'POST'])
def upload_zip_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')

            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(UPLOAD_FOLDER)
            path = path[:-4]
            timeSplit(open(path))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''





if __name__ == "__main__":
    app.secret_key = 'secret key'
    app.run(host='10.10.2.91', port=5001)
