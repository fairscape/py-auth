#© 2020 By The Rector And Visitors Of The University Of Virginia

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import requests, flask, json, os, jwt
from functools import wraps

AUTH_SERVICE = os.environ.get("AUTH_SERVICE", "http://clarklab.uvarc.io/auth")
KEY = os.environ.get('AUTH_KEY')
ISSUER = "ors:compute"



def group_level_permission(handler):
    '''
    Function Wrapper to determine if user is allowed to perform request.
    '''

    @wraps(handler)
    def wrapped_handler(ark,*args,**kwargs):

        if os.environ.get("NO_AUTH",False):
            return handler(ark,*args, **kwargs)

        if flask.request.headers.get("Authorization") is None:
            return flask.Response(
                response= json.dumps({"error": "Request Missing Authorization Header"}),
                status=403,
                content_type="application/json"
            )
        if flask.request.headers.get("Authorization") is None:
            encoded_token = flask.request.cookies.get("fairscapeAuth")
        else:
            encoded_token = flask.request.headers.get("Authorization")
        try:
            json_token = jwt.decode(encoded_token, KEY, algorithms='HS256',audience = 'https://fairscape.org')
        except:
            return flask.Response(
                response= json.dumps({"error": "Auth Expired."}),
                status=401,
                content_type="application/json"
            )
        if json_token.get('role',None) == 'admin':
            return handler(ark,*args, **kwargs)
        elif json_token.get('role',None) == 'user' and object_owner(ark,json_token):
            return handler(ark,*args, **kwargs)
        elif json_token.get('role',None) == 'user' and in_group(ark,json_token):
            return handler(ark,*args, **kwargs)
        else:
            return flask.Response(
                    response=json.dumps({"error": "Must be admin or object owner."}),
                    status=401,
                    content_type="application/json"
                    )
    return wrapped_handler
def owner_level_permission(handler):
    '''
    Function Wrapper to determine if user is allowed to perform request.
    '''

    @wraps(handler)
    def wrapped_handler(ark,*args,**kwargs):

        if os.environ.get("NO_AUTH",False):
            return handler(ark,*args, **kwargs)

        if flask.request.headers.get("Authorization") is None:
            return flask.Response(
                response= json.dumps({"error": "Request Missing Authorization Header"}),
                status=403,
                content_type="application/json"
            )
        if flask.request.headers.get("Authorization") is None:
            encoded_token = flask.request.cookies.get("fairscapeAuth")
        else:
            encoded_token = flask.request.headers.get("Authorization")
        try:
            json_token = jwt.decode(encoded_token, KEY, algorithms='HS256',audience = 'https://fairscape.org')
        except:
            return flask.Response(
                response= json.dumps({"error": "Auth Expired."}),
                status=401,
                content_type="application/json"
            )
        if json_token.get('role',None) == 'admin':
            return handler(ark,*args, **kwargs)
        elif json_token.get('role',None) == 'user' and object_owner(ark,json_token):
            return handler(ark,*args, **kwargs)
        else:
            return flask.Response(
                    response=json.dumps({"error": "Must be admin or object owner."}),
                    status=401,
                    content_type="application/json"
                    )
    return wrapped_handler
def user_level_permission(handler):
    '''
    Function Wrapper for all endpoints that checks that an Authorization is present in request headers.
    If not the wrapper will return an error.

    Used for API service calls where a Globus Token is required.
    '''

    @wraps(handler)
    def wrapped_handler(*args, **kwargs):
        if os.environ.get("NO_AUTH",False):
            return handler(*args, **kwargs)

        if flask.request.headers.get("Authorization") is None:
            return flask.Response(
                response= json.dumps({"error": "Request Missing Authorization Header"}),
                status=403,
                content_type="application/json"
            )

        if flask.request.headers.get("Authorization") is None:
            encoded_token = flask.request.cookies.get("fairscapeAuth")
        else:
            encoded_token = flask.request.headers.get("Authorization")
        try:
            json_token = jwt.decode(encoded_token, KEY, algorithms='HS256',audience = 'https://fairscape.org')
        except:
            return flask.Response(
                response= json.dumps({"error": "Auth Expired."}),
                status=401,
                content_type="application/json"
            )
        if json_token.get('role',None) == 'admin':
            return handler(*args, **kwargs)
        if json_token.get('role',None) == 'user':
            return handler(*args, **kwargs)
        else:
            return flask.Response(
                    response=json.dumps({"error": "failed to authorize user"}),
                    status=401,
                    content_type="application/json"
                    )
    return wrapped_handler

def group_get_owner_else(handler):
    '''
    Function Wrapper to determine if user is allowed to perform request.
    '''

    @wraps(handler)
    def wrapped_handler(ark,*args,**kwargs):

        if os.environ.get("NO_AUTH",False):
            return handler(ark,*args, **kwargs)

        if flask.request.headers.get("Authorization") is None:
            return flask.Response(
                response= json.dumps({"error": "Request Missing Authorization Header"}),
                status=403,
                content_type="application/json"
            )
        if flask.request.headers.get("Authorization") is None:
            encoded_token = flask.request.cookies.get("fairscapeAuth")
        else:
            encoded_token = flask.request.headers.get("Authorization")
        try:
            json_token = jwt.decode(encoded_token, KEY, algorithms='HS256',audience = 'https://fairscape.org')
        except:
            return flask.Response(
                response= json.dumps({"error": "Auth Expired."}),
                status=401,
                content_type="application/json"
            )
        if json_token.get('role',None) == 'admin':
            return handler(ark,*args, **kwargs)
        elif json_token.get('role',None) == 'user' and object_owner(ark,json_token):
            return handler(ark,*args, **kwargs)
        elif flask.request.method == 'GET' and in_group(ark,json_token):
            return handler(ark,*args, **kwargs)
        else:
            return flask.Response(
                    response=json.dumps({"error": "Must be admin or object owner."}),
                    status=401,
                    content_type="application/json"
                    )
    return wrapped_handler

def admin_level_permission(handler):
    '''
    Function Wrapper for all endpoints that checks that an Authorization is present in request headers.
    If not the wrapper will return an error.

    Used for API service calls where a Globus Token is required.
    '''

    @wraps(handler)
    def wrapped_handler(*args, **kwargs):
        if os.environ.get("NO_AUTH",False):
            return handler(*args, **kwargs)

        if flask.request.headers.get("Authorization") is None:
            return flask.Response(
                response= json.dumps({"error": "Request Missing Authorization Header"}),
                status=403,
                content_type="application/json"
            )
        if flask.request.headers.get("Authorization") is None:
            encoded_token = flask.request.cookies.get("fairscapeAuth")
        else:
            encoded_token = flask.request.headers.get("Authorization")
        try:
            json_token = jwt.decode(encoded_token, KEY, algorithms='HS256',audience = 'https://fairscape.org')
        except:
            return flask.Response(
                response= json.dumps({"error": "Auth Expired."}),
                status=401,
                content_type="application/json"
            )
        if json_token.get('role',None) == 'admin':
            return handler(*args, **kwargs)
        else:
            return flask.Response(
                    response=json.dumps({"error": "failed to authorize user"}),
                    status=401,
                    content_type="application/json"
                    )
    return wrapped_handler

def object_owner(ark,json_token):

    try:
        resource = requests.get(AUTH_SERVICE + '/resource/' + ark).json()
    except:
        return False

    if resource['owner'] == json_token['sub']:
        return True

    return False

def in_group(ark,json_token):

    try:
        resource = requests.get(AUTH_SERVICE + '/resource/' + ark).json()
    except:
        return False
        
    user_group = json_token.get('groups',None)
    if user_group is None:
        return False
    resource_group = resource.get('group',None)
    if resource_group is None:
        return False

    if isinstance(user_group,list):
        if isinstance(resource_group,list):
            for u_group in user_group:
                if u_group in resource_group:
                    return True
            return False
        else:
            if resource_group in user_group:
                return True
            return False
    else:
        if isinstance(resource_group,list):
            if user_group in resource_group:
                return True
            return False
        else:
            if user_group == resource_group:
                return True
            return False

    return False
