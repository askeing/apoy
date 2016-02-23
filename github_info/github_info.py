from github import Github


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

    def get_user(self):
        return self.user

    def get_repo_info(self, full_name_or_id):
        return GithubRepoInfo(self.g.get_repo(full_name_or_id))
