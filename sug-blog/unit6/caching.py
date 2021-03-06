import handler.handler as handler


class CachingHandler(handler.TemplateHandler):
    """
    CachingHandler inherits from the hander.TemplateHandler class.
    It displays an information page about caching.
    """
    def get(self):
        self.render("caching.html")
