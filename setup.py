import os
from setuptools import setup, find_packages


VERSION = '0.0.1'

install_requires = [
    'PyGithub',
    'tornado',
]

here = os.path.dirname(os.path.abspath(__file__))
# get documentation from the README and HISTORY
try:
    with open(os.path.join(here, 'README.rst')) as doc:
        readme = doc.read()
except:
    readme = ''

try:
    with open(os.path.join(here, 'HISTORY.rst')) as doc:
        history = doc.read()
except:
    history = ''

long_description = readme + '\n\n' + history

if __name__ == '__main__':
    setup(
        name='github-info',
        version=VERSION,
        description='Get the Github repo\'s information',
        long_description=long_description,
        keywords='github api ',
        author='Askeing Yen',
        author_email='askeing@gmail.com',
        url='https://github.com/askeing/github-info',
        packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
        package_data={},
        install_requires=install_requires,
        zip_safe=False,
        entry_points="""
        # -*- Entry points: -*-
        [console_scripts]
        github_info = github_info.server:main
        """,
    )
