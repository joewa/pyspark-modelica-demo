# Package for the entry points of the Modelica models.
import pkg_resources
import os
import sys


print("in MM")
THIS_DIR = pkg_resources.resource_filename(__name__, ".")

if 'LD_LIBRARY_PATH' not in os.environ:
    os.environ['LD_LIBRARY_PATH'] = os.path.join(THIS_DIR, 'build')
else:
    if os.path.join(THIS_DIR, 'build') not in os.environ['LD_LIBRARY_PATH']:
        os.environ['LD_LIBRARY_PATH'] += os.pathsep + os.path.join(THIS_DIR, 'build')
