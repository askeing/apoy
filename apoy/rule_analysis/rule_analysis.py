#!/usr/bin/python
import os
import shutil
from framework import FrameworkParser


def find_all(path, target):
    res = []
    for root, dirs, fnames in os.walk(path):
        for fname in fnames:
            for line, content in enumerate(open(os.path.join(root, fname))):
                # case insensitive
                content = content.lower()
                if target in content:
                    res.append("{0} found in line: {1} of file: {2}".format(
                                target, line + 1, fname))
    return res


def find(path, target):
    res = []
    for root, dirs, fnames in os.walk(path):
        for fname in fnames:
            for line, content in enumerate(open(os.path.join(root, fname))):
                # case insensitive
                content = content.lower()
                if target in content:
                    res.append("{0} found in line: {1} of file: {2}".format(
                                target, line + 1, fname))
                    return res


def login_handler(repo_summary):
    path = repo_summary['repo_path']
    res = find(path, 'login')
    if res:
        return True
    return False


def forgot_password_handler(repo_summary):
    path = repo_summary['repo_path']
    res = find(path, 'forgot password')
    if res:
        return True
    return False


def todo_handler(repo_summary):
    path = repo_summary['repo_path']
    res = find(path, 'todo')
    if res:
        return True
    return False


def register_handler(repo_summary):
    path = repo_summary['repo_path']
    res = find(path, 'register')
    if res:
        return True
    return False


# predefined rule handlers
rule_handlers = {'login': login_handler,
                 'forgot_password': forgot_password_handler,
                 'todo': todo_handler,
                 'react': FrameworkParser.react_handler,
                 'angular': FrameworkParser.angular_handler,
                 }


def cleanup(input_path):
    shutil.rmtree(input_path)


def run_analysis(repo_summary):
    repo_path = repo_summary['repo_path']
    print repo_path
    enabled_attributes = {k: True for k, v in rule_handlers.items()
                          if v(repo_summary)}
    cleanup(repo_path)
    print("enabled attributes: {}".format(enabled_attributes))
    return enabled_attributes


def main():
    # please git clone Repo before running this testing...
    repo_path = '/temp/angular-registration-login-example'
    return run_analysis({'repo_path': repo_path})

if __name__ == '__main__':
    print(main())
