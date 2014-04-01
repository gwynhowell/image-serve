from google.appengine.api import urlfetch
from google.appengine.ext import db
import webapp2

class Stock(db.Model):
    ticker = db.StringProperty()
    picture = db.BlobProperty(default=None)

class ServeImage(webapp2.RequestHandler):
    def get(self):
        key = self.request.get('key')
        image = Stock.get(key)
        if image:
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.out.write(image.picture)
        else:
            self.abort(404)
      
class CreateDefaults(webapp2.RequestHandler):
    def get(self):
        urls = [
#                'http://www.eso.org/public/archives/images/screen/eso1322a.jpg',
                'http://www.eso.org/public/archives/images/medium/eso0848a.jpg',
                'http://www.eso.org/public/archives/images/medium/eso1006a.jpg',
                'http://www.eso.org/public/archives/images/medium/eso0907a.jpg']
        for url in urls:
            response = urlfetch.fetch(url)
            Stock(picture=response.content).put()
      
class MainPage(webapp2.RequestHandler):
    def get(self):
        images = Stock.all().fetch(100)
        html = ['<img src="/image?key=%s" />' % img.key() for img in images]
        self.response.out.write(html)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/image', ServeImage),
    ('/create_defaults', CreateDefaults),
], debug=True)