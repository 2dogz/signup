#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import os
import re
import webapp2
import jinja2
from google.appengine.ext import db

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Index(webapp2.RequestHandler):
    form = """
    <form method="post">
                <table>
                    <tr>
                        <td><label for="username">Username</label></td>
                        <td>
                            <input name="username" type="text" value="" required>
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="password">Password</label></td>
                        <td>
                            <input name="password" type="password" required>
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="verify">Verify Password</label></td>
                        <td>
                            <input name="verify" type="password" required>
                            <span class="error"></span>
                    </td>
                    </tr>
                    <tr>
                        <td><label for="email">Email (optional)</label></td>
                        <td>
                            <input name="email" type="email" value="">
                            <span class="error"></span>
                        </td>
                    </tr>
                </table>
            <input type="submit">
        </form>
"""
    def get(self):
        self.response.out.write(self.form)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')



        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            #redisplay the form and params
            self.render('signup-form.html', **params)
        else:
            self.redirect('/unit2/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/unit2/signup')

app = webapp2.WSGIApplication([
    ('/', Index),
], debug=True)
