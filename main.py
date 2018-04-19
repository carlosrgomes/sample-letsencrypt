import logging

from flask import Flask
import flask


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/.well-known/acme-challenge/<challenge>')
def letsencrypt_check(challenge):
    print(challenge)
    challenge_response = {
        "J_Y_SHt8Pcvd6aFDtvhvunP2z99YGJj8kDeDRpCU6xg":"J_Y_SHt8Pcvd6aFDtvhvunP2z99YGJj8kDeDRpCU6xg.89n5ovJLN0aPGfXjM5TBFporRo0qvYDmO4nwmbvUxFk",
        "<challenge_token>":"<challenge_response>"
    }
    return flask.Response(response= challenge_response[challenge], status=200, mimetype='text/plain')

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
