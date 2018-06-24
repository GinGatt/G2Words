from frequency import app
from flask import render_template


@app.route('/')
def get_file_drop_display():
    return render_template('filedrop.html')
