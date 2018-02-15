import re
import handler.handler as handler

PASSWORD_RE = re.compile(r"^.{3,20}$")
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


def valid_username(username):
    """
    Validate an input username against a regular expression
    :param username: input username
    :return: true if the username verifies, false otherwise
    """
    return username and USER_RE.match(username)


def valid_password(password):
    """
    Validate an input password against a regular expression
    :param password: input password
    :return: true if the password verifies, false otherwise
    """
    return password and PASSWORD_RE.match(password)


def valid_cfpassword(password, cfpassword):
    """
    Validate an input password and its confirmation against a regular expression
    :param password: input password
    :param cfpassword: confirmed password
    :return: the result of the verification
    """
    result = False
    if valid_password(password):
        result = password == cfpassword
    return result


def valid_email(email):
    """
    Validate an input email against a regular expression
    :param email: input email
    :return: true if the email verifies, false otherwise
    """
    return not email or EMAIL_RE.match(email)


def validate_user(username, password, cfpassword, email):
    """
    Validate user input information
    :param username: input username
    :param password: input password
    :param cfpassword: confirmed password
    :param email: inoput email
    :return: true if all the information is valid, false otherwise
    """
    result = valid_username(username) and valid_password(password)
    result = result and valid_cfpassword(password, cfpassword)
    result = result and valid_email(email)
    return result


class SignupHandler(handler.TemplateHandler):
    """
        SignupHandler inherits from the hander.TemplateHandler class.
        It aggregates methods that offer users the possibility to signup for an account.
    """

    def get(self):
        self.render("signup.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        cfpassword = self.request.get('cfpassword')
        user_email = self.request.get('email')
        comments = self.request.get('comments')

        if validate_user(username, password, cfpassword, user_email):
            self.redirect('/welcome?username=' + username)
        else:
            username_error = ""
            password_error = ""
            cfpassword_error = ""
            email_error = ""

            if not valid_username(username):
                username_error = "Invalid username."
            if not valid_password(password):
                password_error = "Invalid password."
            if not valid_cfpassword(password, cfpassword):
                cfpassword_error = "Your passwords don't match."
            if not valid_email(user_email):
                email_error = "Invalid email."
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
    def get(self):
        user = self.request.get('username')
        if valid_username(user):
            self.render("welcome.html", username=user)
        else:
            self.redirect('/signup')
