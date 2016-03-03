#!/usr/bin/python
import os


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


def run_analysis(repo_summary):
    # rule_handlers = {key: predefined_handlers[key] for key in attributes}
    #repo_path = dump_repo_snapshot(repo_summary['full_name'])
    #summary = repo_summary.copy()
    #summary['repo_path'] = repo_path
    #enabled_attributes = {k: True for k, v in rule_handlers.items()
    #                      if v(summary)}
    #cleanup(repo_path)
    # FIXME: remove this print
    #print("enabled attributes: ")
    #return enabled_attributes
    pass


def main():
    return run_analysis({'full_name': 'zapion/MozITP'})


if __name__ == '__main__':
    print(main())
