import subprocess

__title__ = 'HWUT'
__summary__ = 'Hardware Unit Testing'
__uri__ = 'https://hwut.de/'

__version__ = '0.0.1'

__author__ = 'Raphael Lehmann'
__email__ = 'raphael+hwut@rleh.de'

__license__ = 'AGPLv3'

try:
    git_hash = subprocess.check_output(['git', 'describe', '--always'])
except:
    pass

try:
    git_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
except:
    pass
