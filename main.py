# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
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
# [END app]
