import os
import json
import time
import urllib
import logging
import urlparse

import tornado.ioloop
import tornado.web
from tornado.escape import json_encode
from tornado.httpclient import HTTPClient
from github import UnknownObjectException

from github_info import GithubInfo
from task_worker import TaskWorker


logger = logging.getLogger(__name__)


logging.getLogger('apoy.server').setLevel(logging.INFO)
logging.getLogger('apoy.github_info').setLevel(logging.INFO)
logging.getLogger('apoy.task_worker').setLevel(logging.INFO)
logging.getLogger('apoy.rule_analysis').setLevel(logging.INFO)


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
_HOME_PAGE = '/'
_RESULT_PAGE = '/result'


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    def get(self):
        self.clear_cookie('repoUrl')
        self.render(_STATIC_HTML + 'main.html', title='Apoy')


class LoginHandler(BaseHandler):
    def get(self):
        data = {k: self.get_argument(k) for k in self.request.arguments}
        state = _RESULT_PAGE
        if 'state' in data:
            state = data.get('state')
        if 'repoUrl' in data:
            self.set_secure_cookie('repoUrl', data.get('repoUrl'))
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
        self.clear_cookie('repoUrl')
        self.redirect(_HOME_PAGE)
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

        # if no repoUrl attribute, back to home page
        repo_url = self.get_secure_cookie('repoUrl')
        if not repo_url:
            self.redirect(_HOME_PAGE)
        repo_fullname = urlparse.urlparse(repo_url).path[1:]

        # Create New Task for generating test cases
        taskid = int(time.time())
        gh = GithubInfo(self.get_secure_cookie('github_token'))
        try:
            project_repo_summary = gh.get_repo_info_summary_with_snapshot(repo_fullname)
            TaskWorker(project_repo_summary, taskid).start()
        except UnknownObjectException as e:
            logger.error(e)
            error_msg = 'Get error from {0} repo: {1}'.format(repo_fullname, e.data)
            error = {'error_msg': error_msg}
            url = '{}?{}'.format(_HOME_PAGE, urllib.urlencode(error))
            self.redirect(url)
            return

        # if has state, redirect to that page with taskid
        if state:
            parameters = {'taskid': taskid}
            url = '{}?{}'.format(state, urllib.urlencode(parameters))
            self.redirect(url)


class ResultHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect(_HOME_PAGE)
            return

        self.render(_STATIC_HTML + 'result.html')


class TestHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect(_HOME_PAGE)
            return

        # get cookie for storing access token
        gh = GithubInfo(self.get_secure_cookie('github_token'))

        user = tornado.escape.xhtml_escape(self.current_user)
        name = gh.get_user().get_name()
        email = gh.get_user().get_email()
        location = gh.get_user().get_location()
        self.render(_STATIC_HTML + 'test.html', user=user, name=name, email=email, location=location)


class TaskHandler(BaseHandler):
    def get(self, taskid):
        self.get_task_info(taskid)

    def get_task_info(self, taskid):
        # Using xhr will not have current user
        try:
            with open('results/{}.json'.format(taskid), 'r') as f:
                result = {
                    'user': self.get_current_user(),
                    'id': taskid,
                    'status': 'done',
                    'results': json.load(f)
                }

        except:
            result = {
                'user': self.get_current_user(),
                'id': taskid,
                'status': 'in progress',
                'results': []
            }

        self.write(json.dumps(result))

class RepoInfoHandler(BaseHandler):
    def get(self):
        self.get_repo_info()

    def post(self):
        self.get_repo_info()

    def get_repo_info(self):
        # if not login, redirect to home page
        if not self.current_user:
            self.redirect(_HOME_PAGE)
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

    @staticmethod
    def check_repoinfo(data):
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
        (r'/result', ResultHandler),
        (r'/test', TestHandler),
        (r'/rest/repoinfo', RepoInfoHandler),
        (r'/rest/task/([0-9]+)', TaskHandler),
    ], **settings)


def main():
    app = make_app()
    app.listen(8888)
    print('Start tornado...')
    print('Please open your ngrok url instead of localhost')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
