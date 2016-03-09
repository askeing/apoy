import os
import unittest
from apoy.rule_analysis.framework import FrameworkParser


__author__ = 'Askeing'


class FrameworkTest(unittest.TestCase):
    def setUp(self):
        self.current_dir = os.path.dirname(__file__)
        self.react_dir = os.path.join(self.current_dir, 'react')
        self.angular_dir = os.path.join(self.current_dir, 'angular')

    # Has React
    def test_has_react_dependencies(self):
        path = self.react_dir
        self.assertTrue(FrameworkParser.has_react_dependencies(path))

    def test_has_react_require_in_js(self):
        path = self.react_dir
        self.assertTrue(FrameworkParser.has_react_require_in_js(path))

    def test_react_handler(self):
        path = self.react_dir
        self.assertTrue(FrameworkParser.react_handler(path))

    # No React
    def test_no_react_dependencies(self):
        path = self.angular_dir
        self.assertFalse(FrameworkParser.has_react_dependencies(path))

    def test_no_react_require_in_js(self):
        path = self.angular_dir
        self.assertFalse(FrameworkParser.has_react_require_in_js(path))

    def test_react_handler_false(self):
        path = self.angular_dir
        self.assertFalse(FrameworkParser.react_handler(path))

    # Has Angular
    def test_has_angular_dependencies(self):
        path = self.angular_dir
        self.assertTrue(FrameworkParser.has_angular_dependencies(path))

    def test_has_angular_script_in_html(self):
        path = self.angular_dir
        self.assertTrue(FrameworkParser.has_angular_script_in_html(path))

    def test_angular_handler(self):
        path = self.angular_dir
        self.assertTrue(FrameworkParser.angular_handler(path))

    # No Angular
    def test_no_angular_dependencies(self):
        path = self.react_dir
        self.assertFalse(FrameworkParser.has_angular_dependencies(path))

    def test_no_angular_script_in_html(self):
        path = self.react_dir
        self.assertFalse(FrameworkParser.has_angular_script_in_html(path))

    def test_angular_handler_flase(self):
        path = self.react_dir
        self.assertFalse(FrameworkParser.angular_handler(path))


if __name__ == '__main__':
    unittest.main()
