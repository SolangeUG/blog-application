import handler.handler as handler


class HelloHandler(handler.TemplateHandler):
    """
    HelloHandler inherits from the hander.TemplateHandler class.
    Its sole purpose is to render a page that says "Hello, Udacity!"
    """
    def get(self):
        self.render("hello.html")
