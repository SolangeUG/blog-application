import handler.handler as handler
from google.appengine.ext import db
import urllib


class BlogHandler(handler.TemplateHandler):
    """
    BlogHandler inherits from the hander.TemplateHandler class.
    It aggregates functionalities for creating and retrieving blog posts, using the GAE Datastore.
    """

    def get(self):
        entries = db.GqlQuery('SELECT * FROM Entry ORDER BY created DESC')
        self.render("blog.html", entries=entries)


class BlogEntryHandler(handler.TemplateHandler):
    """
    BlogEntryHandler inherits from the hander.TemplateHandler class.
    It represents a new blog post/entry.
    """
    def render_newentry(self, subject="", entry="", error=""):
        self.render("newentry.html", subject=subject, entry=entry, error=error)

    def get(self):
        self.render_newentry()

    def post(self):
        subject = self.request.get('subject')
        entry = self.request.get('content')

        if subject and entry:
            new_entry = Entry(subject=subject, content=entry)
            new_entry_key = new_entry.put()
            self.redirect('/permalink?entry_key=' + str(new_entry_key))
        else:
            error = "We need both a subject and valid non-empty content!"
            self.render_newentry(subject, entry, error)


class PermalinkHandler(handler.TemplateHandler):
    """
    PermalinkHandler inherits from the hander.TemplateHandler class.
    It represents the last created blog entry.
    """
    def get(self):
        entry_key = db.Key(self.request.get('entry_key'))
        print entry_key
        if entry_key:
            entry = db.get(entry_key)
        else:
            query = db.Query(Entry)
            query.order('-created')
            entry = query.get()
        self.render("permalink.html", entry=entry)


class Entry(db.Model):
    """
    This class inherits from the GAE db.Model (entity) class, and represents a blog entry/post.
    A blog entry is made of three properties:
        - subject : topic/title of the blog entry
        - content : actual content of the blog entry
        - created : creation date and time of blog entry
    """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
