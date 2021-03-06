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


#def get_posts(limit = 0, offset = 0):
    #qry = "SELECT * FROM Blog ORDER BY created DESC LIMIT %s OFFSET %s" % (limit, offset).

    #r = db.GqlQuery(qry)
    #return r

class Blog(db.Model):
    title = db.StringProperty(required=True)
    entry = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):

        error = self.request.get("error")
        title = self.request.get("title")
        entry = self.request.get("entry")
        page = self.request.get("page")

        posts_per_page = 5
        off = posts_per_page * page


        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")
        #blogs = get_posts(posts_per_page, off)

        t = jinja_env.get_template("most_recent.html")
        response = t.render(
                        blogs = blogs,
                        error = error)
        self.response.write(response)



class NewPost(webapp2.RequestHandler):

    def get(self):

        error = self.request.get("error")
        title = self.request.get("title")
        entry = self.request.get("entry")

        t = jinja_env.get_template("add_form.html")
        response = t.render(
                        title = title,
                        entry = entry,
                        error = error)
        self.response.write(response)

    def post(self):

        error = self.request.get("error")
        title = self.request.get("title")
        entry = self.request.get("entry")

        if title and entry:

            b = Blog(title = title, entry = entry)
            b.put()
            c = str(b.key().id())

            self.redirect("/blog/" + c )

        else:

            error = "We need both a title and an entry to create a new blog post."

            t=jinja_env.get_template("add_form.html")
            response = t.render(title = title, entry = entry, error = error)
            self.response.write(response)


class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        a = int(id)

        display = Blog.get_by_id(a)

        if not display:
            error = "That post does not exist."

            t= jinja_env.get_template("most_recent.html")
            response = t.render(error = error)
            self.response.write(response)

        else:

            t= jinja_env.get_template("single_post.html")
            response = t.render(display = display)
            self.response.write(response)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', MainHandler),
    ('/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
