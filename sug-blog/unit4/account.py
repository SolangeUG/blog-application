import handler.handler as handler
import util.security as security
import util.validator as validator
from google.appengine.ext import db


class AccountHandler(handler.TemplateHandler):
    """
    AccountHandler inherits from the hander.TemplateHandler class.
    It gives users the possibility to signup for, or log into, an account.
    """
    def get(self):
        self.render("accounts.html")


class SignupHandler(handler.TemplateHandler):
    """
    SignupHandler inherits from the hander.TemplateHandler class.
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

            # check if the input username is unique
            query = db.Query(Account)
            query.filter('username =', username)
            known_account = query.get()

            if known_account:
                # ask the user to choose a different username
                username_error = "Username already exists"
                self.render("signup.html", username=username, username_error=username_error)
            else:
                # create and persist an account for the user
                hashed_password = security.hash_password(password)
                new_account = Account(username=username, password=hashed_password, email=user_email, comments=comments)
                key = new_account.put()

                self.response.headers['Content-Type'] = 'text/plain'
                # set a cookie with the username
                user_cookie = security.make_secure_val(username)
                self.response.set_cookie('user', str(user_cookie), max_age=3600, path='/')
                self.response.set_cookie('account_key', str(key), max_age=360, path='/')
                self.redirect('/account_created')

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
        user_cookie = self.request.cookies.get('user')
        account_key = self.request.cookies.get('account_key')

        # retrieve username from cookie
        if user_cookie:
            username = security.check_secure_val(user_cookie)

            # retrieve user account by their username from the datastore
            query = db.Query(Account)
            query.filter('username =', username)
            account = query.get()

            # if the above attempt doesn't work, try retrieving by the account key
            if not account:
                if account_key:
                    account_key = db.Key(account_key)
                    account = db.get(account_key)

            # make sure we have a valid account before proceeding
            if account:
                self.render("account.html", username=account.username,
                            email=account.email, creation_date=account.created, comments=account.comments)
            else:
                if user_cookie:
                    # in case the user couldn't be found but a cookie with a username had been set
                    self.response.unset_cookie('user')
                if account_key:
                    # in case the user couldn't be found but a cookie with an account key had been set
                    self.response.unset_cookie('account_key')

                username_error = "Unknown username: " + username
                self.render("login.html", username_error=username_error)
        else:
            self.redirect('/account_signup')

    def post(self):
        # when the logout button is clicked, redirect to the logout page
        self.redirect('/account_logout')


class LoginHandler(handler.TemplateHandler):
    """
    LoginHandler inherits from the handler.TemplateHandler class.
    It aggregates methods that let users sign into and view their account information.
    """
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        if username and password:
            # retrieve user from the datastore
            query = db.Query(Account)
            query.filter('username =', username)
            account = query.get()

            if account:
                # verify input password
                if security.check_password(password, account.password):
                    self.response.headers['Content-Type'] = 'text/plain'

                    # set a cookie with the username
                    user_cookie = security.make_secure_val(account.username)
                    self.response.set_cookie('user', str(user_cookie), max_age=3600, path='/')
                    self.redirect("/account_created")
                else:
                    # the input password is not valid
                    message = "Invalid password!"
                    self.render("login.html", password_error=message)
            else:
                # the input username is unknown
                message = "Invalid username!"
                self.render("login.html", username_error=message)
        else:
            # no username or password were input
            self.render("login.html", username_error="Please input valid usename!",
                        password_error="Please input valid password!")


class LogoutHandler(handler.TemplateHandler):
    """
    LoginHandler inherits from the handler.TemplateHandler class.
    It allows users to sign out of their accounts.
    """
    def get(self):
        # clear out any account cookie that might have been set
        self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/' % str())
        self.response.headers.add_header('Set-Cookie', 'account_key=%s; Path=/' % str())
        # all we ever do from here is go back to the general accounts page
        self.redirect('/account')


class Account(db.Model):
    """
    This class inherits from the GAE db.Model (entity) class, and represents a user account.
    A user account is made of the following properties:
        - username : the username chosen by the user
        - password : the hashed value of the password chosen by the user
        - email : the user's email address
        - comments : the user's comments upon account creation
        - created : creation date and time of user account
    """
    username = db.StringProperty(required=True, indexed=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    comments = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
