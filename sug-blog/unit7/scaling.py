import handler.handler as handler


class ScalingHandler(handler.TemplateHandler):
    """
    ScalingHandler inherits from the hander.TemplateHandler class.
    It displays an information page about scaling up a web application.
    """
    def get(self):
        self.render("scaling.html")
