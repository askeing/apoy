import os
import re
import fnmatch
import logging


__author__ = 'Askeing'
logger = logging.getLogger(__name__)


class FrameworkParser:

    def __init__(self):
        pass

    @staticmethod
    def find(name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)

    @staticmethod
    def find_all(pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result

    @staticmethod
    def has_string(pattern, filename):
        with open(filename, 'r') as f:
            for line in f:
                re_pattern = re.compile(pattern)
                ret = re_pattern.search(line)
                if ret:
                    return True
        return False

    @staticmethod
    def _get_package_json(path):
        return FrameworkParser.find('package.json', path)

    @staticmethod
    def _package_has_react(path):
        return FrameworkParser.has_string('react', path)

    @staticmethod
    def has_react_dependencies(path):
        """
        find "react" in package.json, return True/False.
        """
        package_path = FrameworkParser._get_package_json(path)
        if package_path:
            if FrameworkParser._package_has_react(package_path):
                logger.debug('Find react from {}'.format(package_path))
                return True
            else:
                logger.debug('Cannot find react from {}.'.format(package_path))
        else:
            logger.debug('Cannot find package.json file at {}.'.format(path))
        return False

    @staticmethod
    def _get_bower_json(path):
        return FrameworkParser.find('bower.json', path)

    @staticmethod
    def _bower_has_angular(path):
        return FrameworkParser.has_string('angular', path)

    @staticmethod
    def has_angular_dependencies(path):
        """
        find "angular" in brower.json, return True/False.
        """
        package_path = FrameworkParser._get_bower_json(path)
        if package_path:
            if FrameworkParser._bower_has_angular(package_path):
                logger.debug('Find angular from {}'.format(package_path))
                return True
            else:
                logger.debug('Cannot find angular from {}.'.format(package_path))
        else:
            logger.debug('Cannot find bower.json file at {}.'.format(path))
        return False

    @staticmethod
    def has_react_require_in_js(path):
        """
        find "require('React')" in js files, return True/False.
        """
        js_files = FrameworkParser.find_all('*.js', path)
        if len(js_files) == 0:
            logger.debug('Cannot find andy *.js files at {}'.format(path))
            return False
        for js in js_files:
            if FrameworkParser.has_string(r"require\([\'\"]React[\'\"]\)", js):
                logger.debug('Find react in js file {}'.format(js))
                return True
        logger.debug('Cannot find react in js files')
        return False

    @staticmethod
    def has_angular_script_in_html(path):
        """
        find "require('React')" in js files, return True/False.
        """
        html_files = FrameworkParser.find_all('*.html', path)
        if len(html_files) == 0:
            logger.debug('Cannot find andy *.html files at {}'.format(path))
            return False
        for html in html_files:
            if FrameworkParser.has_string(r"angular(\.min)*\.js", html):
                logger.debug('Find angular in html file {}'.format(html))
                return True
        logger.debug('Cannot find angular in html files')
        return False

    @staticmethod
    def react_handler(repo_path):
        path = repo_path
        # if find framework from dependencies, return True
        if FrameworkParser.has_react_dependencies(path):
            return True

        # find all js files, and then if the react exist, return True
        if FrameworkParser.has_react_require_in_js(path):
            return True
        return False

    @staticmethod
    def angular_handler(repo_path):
        path = repo_path

        # if find framework from dependencies, return True
        if FrameworkParser.has_angular_dependencies(path):
            return True

        # find all html files, and then if the angular exist, return True
        if FrameworkParser.has_angular_script_in_html(path):
            return True
        return False


def main():
    path = './tests/react'
    #path = '/Users/Askeing/software/apoy/temp/todomvc/examples/react'
    print('\n### React Project ###')
    print('- react dep: ' + str(FrameworkParser.has_react_dependencies(path)))
    print('- react js: ' + str(FrameworkParser.has_react_require_in_js(path)))
    print('=> react Handler: ' + str(FrameworkParser.react_handler(path)))
    print('- angular dep: ' + str(FrameworkParser.has_angular_dependencies(path)))
    print('- angular html: ' + str(FrameworkParser.has_angular_script_in_html(path)))
    print('=> angular Handler: ' + str(FrameworkParser.angular_handler(path)))

    path = './tests/angular'
    #path = '/Users/Askeing/software/apoy/temp/angular-registration-login-example'
    print('\n### Angular Project ###')
    print('- react dep: ' + str(FrameworkParser.has_react_dependencies(path)))
    print('- react js: ' + str(FrameworkParser.has_react_require_in_js(path)))
    print('=> react Handler: ' + str(FrameworkParser.react_handler(path)))
    print('- angular dep: ' + str(FrameworkParser.has_angular_dependencies(path)))
    print('- angular html: ' + str(FrameworkParser.has_angular_script_in_html(path)))
    print('=> angular Handler: ' + str(FrameworkParser.angular_handler(path)))


if __name__ == '__main__':
    main()
