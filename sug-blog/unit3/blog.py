import logging
import handler.handler as handler
from google.appengine.ext import db
from google.appengine.api import memcache

# log hits to memcache and hits to the datastore
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def get_blog_entries(update=False):
    """
    Retrieve a list of blog entries from the datastore
    :param update: run the DB query only when it's necessary
    :return: list of blog entries
    """
    # use caching to avoid making DB queries at each page load
    key = 'top'
    entries = memcache.get(key)

    logging.error('MEMCACHE | Blog entries %s' % str(entries))

    if (entries is None) or (len(entries) == 0) or update:
        entries = db.GqlQuery('SELECT * FROM Entry ORDER BY created DESC LIMIT 10')
        entries = list(entries)
        memcache.set(key, entries)

        logging.error('DATASTORE | Blog entries count %s' % str(len(entries)))

    return entries


class BlogHandler(handler.TemplateHandler):
    """
    BlogHandler inherits from the hander.TemplateHandler class.
    It aggregates functionalities for creating and retrieving blog posts, using the GAE Datastore.
    """
    def get(self):
        entries = get_blog_entries()
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

            # rerun the DB query and update the cache
            get_blog_entries(True)

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
        entry_key = self.request.get('entry_key')
        if entry_key:
            entry_key = db.Key(entry_key)
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
