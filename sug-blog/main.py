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
import unit1.hello as hello
import unit2.rot13cipher as cipher
import unit2.signup as form
import unit3.blog as blog
import unit4.account as account
import unit5.apis as apis
import unit6.caching as caching
import unit7.scaling as scaling
import handler.handler as handler


class MainHandler(handler.TemplateHandler):
    """
    MainHandler inherits from the hander.TemplateHandler class.
    This is the entry point of our blog application, all the other handlers will be declared here.
    Each individual handler represents an endpoint to our application.
    """
    def get(self):
        self.render("homepage.html")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/hello', hello.HelloHandler),
    ('/rot13cipher', cipher.Rot13CipherHandler),
    ('/signup', form.SignupHandler),
    ('/welcome', form.WelcomeHandler),
    ('/blog', blog.BlogHandler),
    ('/newentry', blog.BlogEntryHandler),
    ('/permalink', blog.PermalinkHandler),
    ('/account', account.AccountHandler),
    ('/account_signup', account.SignupHandler),
    ('/account_created', account.WelcomeHandler),
    ('/account_login', account.LoginHandler),
    ('/account_logout', account.LogoutHandler),
    ('/apis', apis.BlogAPIHAndler),
    ('/caching', caching.CachingHandler),
    ('/scaling', scaling.ScalingHandler)
], debug=True)
