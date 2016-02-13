# https://github.com/JesseAldridge/flask_simple_login/blob/master/simple_login.py
from flask import session, render_template
from user import User
from database import *
from functools import wraps


def requires_baron(fn):
    @wraps(fn)
    def decorated_function(*a,**kw):
        u = User()
        u.name = session.get('name', None)
        u = get_user(u)
        if not u or not u.isbaron:
            return render_template("not_baron.html", user=get_user_by_name(session.get('name'))), 401
        return fn(*a, **kw)
    return decorated_function


def requires_login(fn):
    @wraps(fn)
    def decorated_function(*a, **kw):
        if not session.get('name', None):
            return render_template("not_logged_in.html", user=get_user_by_name(session.get('name'))), 401
        return fn(*a, **kw)
    return decorated_function


#def require_login(redirect=False):
#    def decorator(fn):
#        @functools.wraps(fn)
#        def decorated_function(*a, **kw):
#            username = session.get('username', None)
#            if not username or username not in g.user_db['user_info']:
#                if redirect:
#                    return flask.redirect('/login')
#                return 'not logged in', 401
#            return fn(*a, **kw)
#        return decorated_function
#    return decorator