import os
import shutil
import logging
from github import Github
from github import UnknownObjectException


logger = logging.getLogger(__name__)


class GithubUserInfo:
    def __init__(self, user_obj):
        self.user = user_obj

    def get_name(self):
        return self.user.name

    def get_login(self):
        return self.user.login

    def get_email(self):
        return self.user.email

    def get_avatar_url(self):
        return self.user.avatar_url

    def get_id(self):
        return self.user.id

    def get_location(self):
        return self.user.location


class GithubRepoInfo:
    def __init__(self, repo_obj):
        self.repo_obj = repo_obj

    def get_language(self):
        return self.repo_obj.language

    def get_languages(self):
        return self.repo_obj.get_languages()

    def get_name(self):
        return self.repo_obj.name

    def get_full_name(self):
        return self.repo_obj.full_name

    def get_description(self):
        return self.repo_obj.description

    def get_owner(self):
        return GithubUserInfo(self.repo_obj.owner)

    def get_file_structure(self):
        depth = 2
        return {'depth': depth, 'result': self._list_path('/', depth=depth)}

    def _list_path(self, path, depth=0):
        result = []
        current = self.repo_obj.get_contents(path)
        for item in current.raw_data:
            item_obj = {
                'name': item['name'],
                'type': item['type'],
                'size': item['size'],
                'path': item['path']
            }
            if (item['type'] == 'dir') and (not depth <= 0):
                    item_obj['sub'] = self._list_path(item_obj['path'], depth - 1)
            result.append(item_obj)
        return result


class GithubInfo:
    def __init__(self, login_or_token=None, password=None):
        assert login_or_token is None or isinstance(login_or_token, (str, unicode)), login_or_token
        assert password is None or isinstance(password, (str, unicode)), password

        self.g = Github(login_or_token=login_or_token, password=password)
        self.user = GithubUserInfo(self.g.get_user())
        self.snapshot = GithubSnapshot()

    def get_user(self):
        return self.user

    def get_repo_info(self, full_name_or_id):
        return GithubRepoInfo(self.g.get_repo(full_name_or_id))

    def get_repo_info_summary(self, full_name_or_id):
        repo = self.get_repo_info(full_name_or_id)
        # if there is no repo name, should raise exception due to there is no repo.
        if not repo.get_name():
            raise UnknownObjectException(200, '{} doesn\'t exist.'.format(full_name_or_id))

        result = {'name': repo.get_name(),
                  'full_name': repo.get_full_name(),
                  'owner.login': repo.get_owner().get_login(),
                  'languages': repo.get_languages(),
                  'description': repo.get_description(),
                  'file_structure': repo.get_file_structure()
                  }
        return result

    def get_repo_info_summary_with_snapshot(self, full_name_or_id, taskid=None):
        result = self.get_repo_info_summary(full_name_or_id)
        repo_path = self.snapshot.dump_repo_snapshot(full_name_or_id, taskid)
        result['repo_path'] = repo_path
        return result


class GithubSnapshot:
    def __init__(self):
        self.snapshot_dir = os.path.abspath(os.path.join('.', 'snapshot'))
        if os.path.exists(self.snapshot_dir) and os.path.isdir(self.snapshot_dir):
            logger.info('The snapshot root folder already exists.')
        else:
            os.mkdir(self.snapshot_dir)
            logger.info('Create snapshot root folder: {}'.format(self.snapshot_dir))

    def dump_repo_snapshot(self, full_name_or_id, taskid=None):
        if taskid:
            root_dir = os.path.join(self.snapshot_dir, str(taskid))
            if os.path.exists(root_dir) and os.path.isdir(root_dir):
                logger.info('The task snapshot folder already exists. TaskID {}'.format(taskid))
            else:
                os.mkdir(root_dir)
                logger.info('Create task snapshot folder: {}'.format(root_dir))
        else:
            root_dir = self.snapshot_dir
        path = os.path.join(root_dir, os.path.basename(full_name_or_id))
        if os.path.exists(path):
            logger.error("Creating snapshot failed for {0}. Path already exists.".format(full_name_or_id))
            return None
        git_repo = "https://github.com/{0}.git".format(full_name_or_id)
        os.system("cd {0}; git clone --depth=1 {1}".format(root_dir, git_repo))
        logger.info('Create snapshot folder: {}'.format(path))
        return path

    def cleanup_repo_snapshot(self, full_name_or_id, taskid=None):
        path = os.path.join(self.snapshot_dir, os.path.basename(full_name_or_id))
        if taskid:
            path = os.path.join(self.snapshot_dir, str(taskid))
        shutil.rmtree(path, ignore_errors=True)
        logger.info('Remove snapshot folder: {}'.format(path))
