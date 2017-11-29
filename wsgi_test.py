from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from wsgiref.validate import validator
 
# an application interface is a callable object: ex. function, instance with an object.__call() method
def simple_app(environ, start_response):
    # its parameters contains:
    # 1) environ: a dictionary containing CGI like variables 
    # 2) start_response: a callback function used to send HTTP status code/message and HTTP headers to the server
    setup_testing_defaults(environ)
 
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
 
    start_response(status, headers)
 
    body = 'hello world' #'<script>alert("hello world")</script>\n'.encode('utf-8')
    return [body]
    # it returns the response body to the server as strings wrapped in an iterable
 
class MyMiddleware(object):
    # a decorator that wraps the application with the same call function parameters: environ & start_response

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        body = self.app(environ, start_response)
        yield '<script>alert(%s)</script>' % body
 
app = MyMiddleware(simple_app)
validator_app = validator(app)
httpd = make_server('', 8000, validator_app)
print('serving on port 8000')
httpd.serve_forever()
# to test, open browser and connect to http://localhost:8000/

# real-world example:
# CacheMiddleware(    -> log the request information
#   RoutesMiddleware( -> decide which controller handles the request
#     App             -> the application that generates the content
#   )
# )
