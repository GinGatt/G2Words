"""
Defines Views (Routes) used by the Flask application
Current Views support uploading a file through direct selection,
identification of dataset, and display of word frequency and location results
"""

import os
from flask import render_template, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
import json
# from .worker import redis_conn
from rq.job import Job
from app import app, q
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


@app.route('/', methods=['GET'])
def index():
    files = list_filenames()
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
def file_upload():
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
            with open(save_path, "r") as f:
                pass
            flash('File Uploaded Successfully')
    files = list_filenames()
    return render_template('index.html', files=files)


@app.route('/start', methods=['POST'])
def get_frequency_and_location():
    frequency_instance = Frequency()
    # start job that will be run in the background and recognized by the worker
    # job = q.enqueue_call(func=frequency_instance.calculate, args=(app.config['UPLOAD_FOLDER'],), result_ttl=5000)
    my_data = frequency_instance.calculate(app.config['UPLOAD_FOLDER'])
    print(my_data)
    return render_template('blank.html', output=my_data)


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    # job = Job.fetch(job_key, connection=redis_conn)
    converted_job_data = job.data.decode('ascii')
    print('type', type(converted_job_data))
    # if job.is_finished:
    sorted_result = sorted(converted_job_data.items(), key=(lambda x: x[1]['count']), reverse=True)[:20]
    print(sorted_result)
    return render_template('blank.html', output='abc')
    # else:
    #     return render_template('blank.html', output='def'), 204
