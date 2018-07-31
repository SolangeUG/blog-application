import handler.handler as handler
import util.validator as validator


class SignupHandler(handler.TemplateHandler):
    """
    SignupHandler inherits from the hander.TemplateHandler class.
    It aggregates methods that offer users the possibility to signup for an account.
    """

    def get(self):
        self.render("signup.html")

    def post(self, check_cookie=False):
        username = self.request.get('username')
        password = self.request.get('password')
        cfpassword = self.request.get('verify')
        user_email = self.request.get('email')
        comments = self.request.get('comments')

        if validator.validate_user(username, password, cfpassword, user_email):
            if check_cookie:
                self.response.headers['Content-Type'] = 'text/plain'

                # TODO: set a cookie with the username

                self.redirect('/welcome')
            else:
                self.redirect('/welcome?username=' + username)
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
                        user_email=user_email,
                        email_error=email_error,
                        comments=comments)


class WelcomeHandler(handler.TemplateHandler):
    """
    WelcomeHandler inherits from the handler.TemplateHandler class.
    Its sole purpose is to confirm user account signup, or redirect
    them to the signup page if the input information isn't valid.
    """
    def get(self, check_cookie=False):
        # case when working with cookies
        if check_cookie:
            print "TODO: check username in coookie"
            user = ''
        # case when the user name is sent as a request parameter
        else:
            user = self.request.get('username')

        if validator.is_username_valid(user):
                self.render("welcome.html", username=user)
        else:
            self.redirect('/signup')
