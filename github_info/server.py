import os
import json
import urllib
import urlparse

import tornado.ioloop
import tornado.web
from tornado.escape import json_encode
from tornado.httpclient import HTTPClient

from github_info import GithubInfo


_STATIC_HTML = 'static/'


def load_settings():
    settings_file = os.path.join(os.path.dirname(__file__), 'settings.json')
    if os.path.isfile(settings_file):
        with open(settings_file) as f:
            settings = json.load(f)
            if 'client_id' not in settings:
                raise Exception('No "client_id" in settings file {}'.format(settings_file))
            if 'client_secret' not in settings:
                raise Exception('No "client_secret" in settings file {}'.format(settings_file))
            return settings
    else:
        raise Exception('No settings file {}\n'
                        'Please open your Github OAuth application page for getting "client_id" and "client_secret".\n'
                        'And then modify the "Authorization callback URL" to your server callback URL.'
                        .format(settings_file))


_SETTINGS = load_settings()
_RESULT_PAGE = 'result'


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    def get(self):
        self.render(_STATIC_HTML + 'main.html', title='Apoy')


# TODO: will be removed after finish all work
class StopHandler(BaseHandler):
    def get(self):
        print('Stopping tornado...')
        tornado.ioloop.IOLoop.instance().stop()
        print('Tornado stopped.')


class LoginHandler(BaseHandler):
    def get(self):
        data = {k: self.get_argument(k) for k in self.request.arguments}
        state = _RESULT_PAGE
        if 'state' in data:
            state = data['state']
        # redirect to Github OAuth page
        oauth_url = 'https://github.com/login/oauth/authorize'
        parameters = {
            'client_id': _SETTINGS.get('client_id'),
            'state': state
        }

        url = oauth_url + '?' + urllib.urlencode(parameters)
        self.redirect(url)
        return


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.clear_cookie('github_token')
        self.redirect('/')
        return


class CallBackHandler(BaseHandler):
    def get(self):
        token_url = 'https://github.com/login/oauth/access_token'
        # get code/state from Github OAuth
        data = {k: self.get_argument(k) for k in self.request.arguments}
        code = data['code']
        state = ''
        if 'state' in data:
            state = data['state']
        parameters = {
            'client_id': _SETTINGS.get('client_id'),
            'client_secret': _SETTINGS.get('client_secret'),
            'code': code,
            'state': state
        }
        body = urllib.urlencode(parameters)
        # get access_token from Github
        http_client = HTTPClient()
        response = http_client.fetch(token_url, method='POST', body=body)
        ret_token = response.body
        token_obj = dict(urlparse.parse_qsl(ret_token))
        # set cookie for storing access token
        self.set_secure_cookie('github_token', token_obj['access_token'])

        # get user login
        gh = GithubInfo(token_obj['access_token'])
        user_login = gh.get_user().get_login()

        # User login
        self.set_secure_cookie('user', user_login)

        # if has state, redirect to that page
        if state:
            self.redirect(state)


class TestHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect('/')
            return

        # get cookie for storing access token
        gh = GithubInfo(self.get_secure_cookie('github_token'))

        user = tornado.escape.xhtml_escape(self.current_user)
        name = gh.get_user().get_name()
        email = gh.get_user().get_email()
        location = gh.get_user().get_location()
        self.render(_STATIC_HTML + 'test.html', user=user, name=name, email=email, location=location)


class RepoInfoHandler(BaseHandler):
    def get(self):
        self.get_repo_info()

    def post(self):
        self.get_repo_info()

    def get_repo_info(self):
        # if not login, redirect to home page
        if not self.current_user:
            self.redirect('/')
            return

        data = {k: self.get_argument(k) for k in self.request.arguments}
        if self.check_repoinfo(data):
            repo_url = data.get('repoUrl')
            repo_fullname = urlparse.urlparse(repo_url).path[1:]

            # get cookie for storing access token
            gh = GithubInfo(self.get_secure_cookie('github_token'))
            result = gh.get_repo_info_summary(repo_fullname)
            self.write(json_encode(result))
        else:
            raise tornado.web.HTTPError(400)

    def check_repoinfo(self, data):
        if 'repoUrl' in data:
            return True
        return False


def make_app():
    cookie_secret = '__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__'
    if 'cookie_secret' in _SETTINGS:
        cookie_secret = _SETTINGS.get('cookie_secret')
    settings = {
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'cookie_secret': cookie_secret,
        'login_url': '/login',
    }

    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/cb', CallBackHandler),
        # (r'/stop', StopHandler),
        (r'/test', TestHandler),
        (r'/rest/repoinfo', RepoInfoHandler),
    ], **settings)


def main():
    app = make_app()
    app.listen(8888)
    print('Start tornado...')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
