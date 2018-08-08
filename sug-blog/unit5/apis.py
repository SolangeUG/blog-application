import json
import datetime
import handler.handler as handler
from google.appengine.ext import db
import util.json_formatter as formatter


class BlogAPIHAndler(handler.TemplateHandler):
    """
    BlogHandler inherits from the hander.TemplateHandler class.
    It displays an information page about designing a pragmatic RESTful API.
    """
    def get(self):
        self.render("apis.html")


class BlogJSONHandler(handler.TemplateHandler):
    """
    BlogHandler inherits from the hander.TemplateHandler class.
    It retrieves blog entries from the datastrore, and returns them in JSON format
    """
    def get(self):
        entries = db.GqlQuery('SELECT * FROM Entry ORDER BY created DESC')
        entries_list = []
        for entry in entries:
            entries_list.append(formatter.format_entry_as_json(entry))
        content = {"content": entries_list, "date": datetime.datetime.now().strftime('%b %d, %Y - %H:%M')}

        # the JSON output could be displayed directly as follows
        # self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        # self.write(json.dumps(content, indent=4, separators=(',', ':')))

        self.render("blog_json.html", entries=json.dumps(content, indent=4, separators=(',', ':')))

