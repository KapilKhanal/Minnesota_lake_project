from api.config import PACKAGE_ROOT
import sys
import os

#sys.path.append((os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
with open(PACKAGE_ROOT / 'VERSION') as version_file:
    __version__ = version_file.read().strip()
