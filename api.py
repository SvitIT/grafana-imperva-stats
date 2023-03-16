from flask import Flask, request, redirect
from log_helper import path_upload
from iozip import ImpervaLog

app = Flask(__name__)

UPLOAD_FOLDER = './stats'
ALLOWED_EXTENSIONS = {'csv', 'zip'}


upload_form = '''
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
    if request.method == 'POST':
        try:
            plain = ImpervaLog(request.files['file']).get_plain_data()
            print()
            # path_upload(w.path)(measurement)
        except (KeyError, AttributeError):
            return redirect(request.url)
    return upload_form


if __name__ == "__main__":
    app.secret_key = 'secret key'
    app.run()
