import handler.handler as handler
import util.security as security
import util.validator as validator
from google.appengine.ext import db


class AccountHandler(handler.TemplateHandler):
    """
    AccountHandler inherits from the hander.TemplateHandler class.
    It aggregates methods that offer users the possibility to create and persist an account.
    """

    def get(self):
        self.render("signup.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        cfpassword = self.request.get('verify')
        user_email = self.request.get('email')
        comments = self.request.get('text')

        if validator.validate_user(username, password, cfpassword, user_email):
            self.response.headers['Content-Type'] = 'text/plain'

            # check if a user cookie has already been set
            username_cookie = self.request.cookies.get('user')
            if username_cookie:
                # make sure the cookie hasn't been tempered with
                known_username = security.check_secure_val(username_cookie)
                if known_username:
                    # do we hava a user associated with the retrieved cookie?
                    account = db.GqlQuery('SELECT * FROM Account WHERE username=%s' % known_username)
                    if account:
                        username_error = "User already exists"
                        self.render("signup.html", username=username, username_error=username_error)
                    else:
                        self.redirect('/account')
                else:
                    username_error = "Invalid cookie value"
                    self.render("signup.html", username=username, username_error=username_error)
            else:
                # set a cookie with the username
                user_cookie = security.make_secure_val(username)
                self.response.headers.add_header('Set-Cookie', 'user=%s' % str(user_cookie))

                # persist user to the datastore
                hashed_password = security.hash_password(password)
                new_account = Account(username=username, password=hashed_password)
                new_account.put()

                self.redirect('/accountcreated')
        else:
            username_error = ""
            password_error = ""
            cfpassword_error = ""
            email_error = ""

            if not validator.is_username_valid(username):
                username_error = "Invalid username!"
            if not validator.is_password_valid(password):
                password_error = "Invalid password!"
            if not validator.is_cfpassword_valid(password, cfpassword):
                cfpassword_error = "Your passwords don't match!"
            if not validator.is_email_valid(user_email):
                email_error = "Invalid email!"
            self.render("signup.html",
                        username=username,
                        username_error=username_error,
                        password_error=password_error,
                        cfpassword_error=cfpassword_error,
                        email=user_email,
                        email_error=email_error,
                        comments=comments)


class WelcomeHandler(handler.TemplateHandler):
    """
    WelcomeHandler inherits from the handler.TemplateHandler class.
    Its sole purpose is to confirm user account signup, or redirect
    them to the signup page if the input information isn't valid.
    """
    def get(self):
        user = None
        user_cookie = self.request.cookies.get('user')

        # retrieve username from cookie
        if user_cookie:
            user = security.check_secure_val(user_cookie)

        # make sure we have a valid username before proceeding
        if validator.is_username_valid(user):
            self.render("welcome.html", username=user)
        else:
            self.redirect('/account')


class Account(db.Model):
    """
    This class inherits from the GAE db.Model (entity) class, and represents a user account.
    A user account is made of the following properties:
        - username : the username chosen by the user
        - password : the hashed value of the password chosen by the user
        - email : the user's email address
        - created : creation date and time of user account
    """
    username = db.StringProperty(required=True, indexed=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
