#!/usr/bin/python
import os
import shutil


def find(path, target):
    res = []
    for root, dirs, fnames in os.walk(path):
        for fname in fnames:
            for line, content in enumerate(open(os.path.join(root, fname))):
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


# predefined rule handlers
rule_handlers = {'login': login_handler,
                 'forgot_password': forgot_password_handler,
                 }

def cleanup(input_path):
    shutil.rmtree(input_path)

def run_analysis(repo_summary):
    repo_path = repo_summary['repo_path']
    print repo_path
    enabled_attributes = {k: True for k, v in rule_handlers.items()
                          if v(repo_summary)}
    cleanup(repo_path)
    print("enabled attributes: ")
    return enabled_attributes


def main():
    return run_analysis({'full_name': 'zapion/MozITP'})


if __name__ == '__main__':
    print(main())
