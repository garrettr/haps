import os
from flask import Flask, url_for, render_template, request, redirect
from werkzeug import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    'uploads')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['POST', 'GET'])
def upload():
    error = None
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_thanks'))
    else:
        return render_template('upload.html')

@app.route('/upload/thanks')
def upload_thanks(filename=None):
    return render_template('upload_thanks.html')

from flask import send_from_directory
@app.route('uploads/file/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'

@app.route('/')
def index():
    return render_template('index.html')

if app.debug:
    # use Flask to serve static files
    with app.test_request_context():
        url_for('static', filename='style.css')

if __name__ == '__main__':
    app.run()
