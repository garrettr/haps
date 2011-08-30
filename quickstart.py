from flask import Flask, url_for, render_template, request
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/', methods=['POST', 'GET'])
def upload():
    error = None
    if request.method == 'POST':
        pass
    else:
        return render_template('upload.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'

if app.debug:
    # use Flask to serve static files
    with app.test_request_context():
        url_for('static', filename='style.css')

if __name__ == '__main__':
    app.run()
