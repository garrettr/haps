# Notes

I implemented a Tor check on the upload page, but cannot test it while the server is running on
localhost. I'm not sure if there exists a way for me to test it until it's running on a proper server.

Currently working on file queue that will be send files to remote file server (Tor hidden
service), along with a bunch of randomly generated garbage files to make end-point correlation
attacks more difficult.

# Quickstart

To get started with working on this code, first clone the repo

    git clone git@github.com:handsomeransoms/haps.git

You will need to install Python library dependencies to use this code. To do this easily and
without cluttering up your system, use [virtualenv]. Here's how to setup virtualenv:

1.  cd into the directory of the cloned repo
2.  `virtualenv env` creates a new virtualenv and installs Python into it.
3.  `. env/bin/activate` activates the virtualenv. You will see `(env)`
    prepended to your bash prompt.
4.  Install the dependencies

Now you need to start beanstalkd, run the worker pythons script, and run the Flask application.
In your shell, first launch beanstalkd as a deamon (`-d` flag). We're using the default IP/port
combo (localhost/11300), so don't worry about passing them in.

1.  `beanstalkd -d`
2.  `python bs-worker.py`
3.  In a separate shell, `python quickstart.py`.
    Navigate to [127.0.0.1:5000] in your browser. Try uploading a file, see it appear in the
    output of bs-worker.py

# Dependencies

You will need to install these:
We recommend using pip: `easy_install pip`, and installing into your virtualenv.

1.  [Flask web microframework]: `pip install flask`
2.  Beanstalkd, a work queue.
    [Install instructions here](http://kr.github.com/beanstalkd/download.html)
    On a mac, you can use Homebrew: brew install beanstalkd
3.  PyYAML (dependency of the Python beanstalk library): `pip install pyyaml`
4.  `pip install beanstalkc`
    Python [library for beanstalkd](https://github.com/earl/beanstalkc/).

[virtualenv]: http://www.arthurkoziel.com/2008/10/22/working-virtualenv/
[Flask web microframework]: http://flask.pocoo.org/
