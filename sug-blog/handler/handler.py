import os
import jinja2
import webapp2

# os.path.dirname(__file__) returns the string name of the current directory ==> 'sug-blog'
# os.path.join(os.path.dirname(__file__), "../pages") appends 'pages' to the current directory ==> 'sug-blogs/pages'
template_dir = os.path.join(os.path.dirname(__file__), "../pages")
jinja_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(template_dir),
                autoescape=True)


class TemplateHandler(webapp2.RequestHandler):
    """
        TemplateHandler inherits from the webapp2.RequestHandler class.
        Its main purpose is to aggregate methods that render a given template,
        with given arguments to the screen.
    """
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    @staticmethod
    def render_str(template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
