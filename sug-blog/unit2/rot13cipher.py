import handler.handler as handler


def rot13_char_limits(char, lower, upper):
    """
    Return an encrypted character using the ROT13 cipher
    :param char: input char
    :param lower: lower bound
    :param upper: upper bound
    :return: the corresponding encrypted character
    """
    result = char
    ord_char = ord(char)
    if lower <= ord_char <= upper:
        if ord_char + 13 <= upper:
            result = chr(ord_char + 13)
        else:
            result = chr(ord_char - 13)
    return result


def rot13_char(char):
    """
    Return an encrypted character using the ROT13 cipher
    :param char: input char
    :return: the corresponding encrypted character
    """
    lower = 0
    upper = 0
    result = char
    if char:
        if char.isupper():
            lower = ord('A')
            upper = ord('Z')
        elif char.islower():
            lower = ord('a')
            upper = ord('z')
        result = rot13_char_limits(char, lower, upper)
    return result


def rot13(text):
    """
    Return an encrypted message using the ROT13 cipher
    :param text: input message
    :return: the corresponding encrypted text
    """
    result = ''
    if text:
        for c in text:
            d = rot13_char(c)
            result = result + d
    return result


class Rot13CipherHandler(handler.TemplateHandler):
    """
        Rot13CipherHandler inherits from the hander.TemplateHandler class.
        It aggregates methods that help cipher (and decipher) a message
        using the ROT13 simple letter substitution cipher.
    """

    def get(self):
        self.render("rot13cipher.html")

    def post(self):
        original_message = self.request.get('text')
        final_message = rot13(original_message)
        self.render("rot13cipher.html", message=final_message)
