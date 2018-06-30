"""
Defines Views (Routes) used by the Flask application
Current Views support uploading a file through direct selection,
identification of dataset, and display of word frequency and location results
"""

import os
from flask import render_template, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
from app import app
from .frequency import Frequency


ALLOWED_EXTENSIONS = ['txt']


def allowed_file(filename):
    """
    Primitive attempt to only allow .txt to be processed
    :param str filename: The name of the file to upload
    :return: true/false of whether allowed file
    :rtype: bool
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def list_filenames():
    """
    Order filenames by time when uploaded.
    Files which were accessed last will be at top of the list
    :return: list of filenames sorted by last accessed (coinciding with last accessed)
    :rtype: list
    """
    files = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        path = os.path.join(app.config['UPLOAD_FOLDER'], file)
        if os.path.isfile(path) and allowed_file(file):
            files.append(file)

    def get_file_access_time(filename):
        filepath = '{0}/{1}'.format(app.config['UPLOAD_FOLDER'], filename)
        file_stats = os.stat(filepath)
        last_access_time = file_stats.st_atime
        return last_access_time

    return sorted(files, key=get_file_access_time)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Not an acceptable file')
            return redirect(request.url)
        elif request.files['file'].filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                # open and close to update the access time for sorting.
                with open(save_path, 'r') as f:
                    pass
                flash('File Uploaded Successfully')
    files = list_filenames()
    return render_template('index.html', files=files)


@app.route('/start', methods=['POST'])
def get_frequency_and_location():
    frequency_instance = Frequency()
    my_data = frequency_instance.calculate(app.config['UPLOAD_FOLDER'])[:15]
    return jsonify(my_data)
