import os
from flask import Flask, url_for, render_template, request, redirect
from werkzeug import secure_filename

# for Tor check
import DNS
DNS.DiscoverNameServers()

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    'uploads')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_client_ip(request):
    ip = None
    # print request.environ
    x_forwarded_for = request.environ.get('X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.environ.get('REMOTE_ADDR')
    return ip

def tor_check(clientIp, ELPort):
    # derived from:
    # https://svn.torproject.org/svn/check/trunk/cgi-bin/TorCheck.py
    # exit node IP
    splitIp = clientIp.split('.')
    splitIp.reverse()
    ELExitNode = ".".join(splitIp)

    # ELPort set by caller - try 80 (HTTP) and 443 (HTTPS)
    
    # We'll try to reach this host
    # -- How is this chosen?
    ELTarget = "38.229.70.31"
    # This is the ExitList DNS server we want to query
    ELHost = "ip-port.org.exitlist.torproject.org"

    # Prepare the question as an A record request
    ELQuestion = ELExitNode + "." + ELPort + "." + ELTarget + "." + ELHost
    request = DNS.DnsRequest(name=ELQuestion, qtype='A')

    # Ask the question, load data into answer
    try:
        answer = request.req()
    except DNS.DNSError:
        return 2

    # Parse the answer, decide if it's allowing exits
    # 127.0.0.2 is an exit and NXDOMAIN is not
    if answer.header['status'] == "NXDOMAIN":
        # We're not exiting from a Tor exit
        return 1
    else:
        if not answer.answers:
            # Unexpected data - fail closed
            return 2
        for a in answer.answers:
            if a['data'] != "127.0.0.2":
                return 2
        # if we're here, that's a positive exit answer
        return 0


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
        client_ip = get_client_ip(request)
        is_using_tor = tor_check(client_ip, "80")
        if is_using_tor != 0:
            # edge case - only HTTPS (port 443) allowed on exit node
            is_using_tor = tor_check(client_ip, "443")
        if is_using_tor == 0:
            is_using_tor = True
        else:
            is_using_tor = False
        return render_template('upload.html', client_ip=client_ip, 
                is_using_tor=is_using_tor)

@app.route('/upload/thanks')
def upload_thanks(filename=None):
    return render_template('upload_thanks.html')

from flask import send_from_directory
@app.route('/uploads/file/<filename>')
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
    # do i really need this?
    with app.test_request_context():
        url_for('static', filename='style.css')

if __name__ == '__main__':
    app.run()
