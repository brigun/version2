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

import webapp2
import os
import jinja2

from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Blog(db.Model):
    title = db.StringProperty(required=True)
    entry = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):

        error = self.request.get("error")
        title = self.request.get("title")
        entry = self.request.get("entry")

        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")

        t = jinja_env.get_template("add_form.html")
        response = t.render(
                        blogs = blogs,
                        error = error)
        self.response.write(response)

    def post(self):

        error = self.request.get("error")
        title = self.request.get("title")
        entry = self.request.get("entry")

        if title and entry:

            b = Blog(title = title, entry = entry)
            b.put()
            self.redirect("/")

        else:

            error = "We need both a title and an entry to create a new blog post."

            self.redirect("/?error=" + error)



app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
