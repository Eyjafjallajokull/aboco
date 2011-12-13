import os
import logging
from multiprocessing import Process
from os import path, curdir, sep
from mimetypes import guess_type
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from core.config import Config
import base64
import re
import urllib2
from datetime import time

_wm = None

class AuthException(Exception):
    pass

class AbocoHTTPServer():
    serverAddress = None
    numberOfProcesses = None
    
    def __init__(self, serverAddress, numberOfProcesses):
        self.serverAddress = serverAddress
        self.numberOfProcesses = numberOfProcesses
        
    def start(self):
        logging.info('Starting HTTP server at %s:%d with %s threads' % 
                     (self.serverAddress[0],
                      self.serverAddress[1], 
                      self.numberOfProcesses))
        
        server = AbocoHTTPThread(self.serverAddress)
        for i in range(self.numberOfProcesses-1):
            Process(target=server.start, args=()).start()
        server.start()
        
    def setWm(self, wm):
        global _wm
        _wm = wm
    

class AbocoHTTPThread(HTTPServer):
    _authenticated = []
    
    def __init__(self, serverAddress):
        HTTPServer.__init__(self, serverAddress, AbocoRequestHandler)

    def start(self):
        logging.debug('started HTTP process %d' % os.getpid())
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            self.stop()
        
    def stop(self):
        logging.debug('stopped HTTP process %d' % os.getpid())
        #self.shutdown()
    
        
class AbocoRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logging.debug('HTTP > %s' % (format % args))
    
    def _writeheaders(self, code=200, contentType='text/html'):
        self.send_response(code)
        self.send_header('Content-type', contentType)
        self.end_headers()
        
    def getHeader(self, name):
        match = re.search(name+': (.+)$', str(self.headers))
        print match
        return match.group( 1 ) if match else 0

    def do_POST(self):
        self._writeheaders(200, 'text/json')
        global _wm
        if self.path == '/update':
            self.wfile.write(_wm.collectData())
            
        '''
        if self.path == '/saveCfg':
            contentLength = self.getHeader('Content-Length')
            data = self.rfile.read(int(contentLength))
            client = Config().setNamespace('client', data)
        '''

    def do_GET(self):
        if self.path == '/':
            #reload config on page reload
            Config().load()
            
            self.handleRootPage()
            
        else:
            self.handleStatic()
        
        
    def handleStatic(self):
        fileName = path.abspath(curdir + sep + self.path)
        rootDir = path.abspath(curdir)
        if not path.isfile(fileName) or not fileName.startswith(rootDir):
            self.send_error(404,'File Not Found: %s' % self.path)
            return
        
        if fileName.endswith('.py') or fileName.endswith('config.json'):
            self.send_error(404,'File Not Found: %s' % self.path)
            return
        
        self._writeheaders(200, guess_type(fileName)[0])
        f = open(fileName, 'rb')
        self.wfile.write(f.read())
        f.close()
        
    def handleRootPage(self):
        self._writeheaders()
        
        styles = ''
        scripts = ''
        
        styleTpl = '<link rel="stylesheet" href="$$">\n'
        scriptTpl = '<script src="$$"></script>\n'
        
        for root, dirs, files in os.walk('widgets'):
            for file in files:
                if file.endswith('.css'):
                    styles += styleTpl.replace('$$', root+os.sep+file)
                if file.endswith('.js'):
                    scripts += scriptTpl.replace('$$', root+os.sep+file)
        
        f = open('core/static/index.html').read()
        f = f.replace('{{styles}}',styles)
        f = f.replace('{{scripts}}',scripts)
        
        f = f.replace('{{core}}',
                      str(Config().getNamespace('core',True)))
        f = f.replace('{{widgets}}',
                      str(Config().getNamespace('widgets',True)))
        self.wfile.write(f)

