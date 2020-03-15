import subprocess

__title__ = 'HWUT'
__summary__ = 'Hardware Unit Testing'
__uri__ = 'https://hwut.de/'

__version__ = '0.0.1'

__author__ = 'Raphael Lehmann'
__email__ = 'raphael+hwut@rleh.de'

__license__ = 'AGPLv3'

git_hash = 'no_git'
try:
    git_hash = subprocess.check_output(['git', 'describe', '--always', '--dirty']).decode('utf-8').strip()
except:
    pass

git_branch = 'no_git'
try:
    git_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()
except:
    pass
