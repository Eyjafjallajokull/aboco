import os
import tornado.ioloop
import tornado.web
from core.config import Config

rootDir = os.path.abspath('./')

class RootHandler(tornado.web.RequestHandler):
    def initialize(self, wm):
        self.wm = wm

    ''' Handle requests to / '''
    def get(self):        
        styles = []
        scripts = []
                
        for root, dirs, files in os.walk('widgets'):
            for file in files:
                if file.endswith('.css'):
                    styles.append(root+os.sep+file)
                elif file.endswith('.js'):
                    scripts.append(root+os.sep+file)
        
        self.render("../public/index.html", 
                    styles=styles, 
                    scripts=scripts,
                    core=str(Config().getNamespace('core',True)),
                    widgets=self.wm.getConfig())

class StaticHandler(tornado.web.RequestHandler):
    ''' Handle requests to static files '''
    def get(self, ignore, ignore2):
        fileName = os.path.abspath(rootDir + os.sep + self.request.path)
        
        if fileName.startswith(rootDir) and os.path.isfile(fileName):
            if fileName.endswith('js'):
                self.set_header("Content-Type", "text/javascript")
            elif fileName.endswith('css'):
                self.set_header("Content-Type", "text/css")
            self.write(open(fileName).read())

class UpdateHandler(tornado.web.RequestHandler):
    ''' Handle ajax requests '''
    def initialize(self, wm):
        self.wm = wm
    
    def post(self):
        self.write( self.wm.collectData() )


class AbocoHTTPServer():
    ''' Tornado HTTP server wrapper '''
    def __init__(self, wm):
        self.wm = wm
        self.application = tornado.web.Application([
            (r"/", RootHandler, dict(wm=wm)),
            (r"^/(public|widgets)/.*?(js|css|png)$", StaticHandler),
            (r"^/update$", UpdateHandler, dict(wm=wm) )
        ])
        
    def start(self):
        ''' start Tornado server '''
        self.application.listen(Config().get('http','port'))
        tornado.ioloop.IOLoop.instance().start()
