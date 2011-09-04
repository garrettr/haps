# Notes

I implemented a Tor check on the upload page, but cannot test it while the server is running on
localhost. I'm not sure if there exists a way for me to test it until it's running on a proper server.

# Quickstart

To get started with working on this code, first clone the repo

    git clone git@github.com:handsomeransoms/haps.git

You will need a working installation of the [Flask web microframework] to work
with this code. The easiest way to do this is with [virtualenv].

1.  cd into the directory of the cloned repo
2.  `virtualenv env` creates a new virtualenv and installs Python into it.
3.  `. env/bin/activate` activates the virtualenv. You will see `(env)`
    prepended to your bash prompt.
4.  Install flask: `easy_install Flask`

Now just `python quickstart.py` to run the application. For more info on
Flask, check out their [excellent docs].

[virtualenv]: http://www.arthurkoziel.com/2008/10/22/working-virtualenv/
[Flask web microframework]: http://flask.pocoo.org/
[excellent docs]: http://flask.pocoo.org/docs/
