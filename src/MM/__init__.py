# Package for the entry points of the Modelica models.
import importlib.resources
import os
import sys

print("in MM")
THIS_DIR = str(importlib.resources.files(__package__ or 'MM'))

if 'LD_LIBRARY_PATH' not in os.environ:
    os.environ['LD_LIBRARY_PATH'] = os.path.join(THIS_DIR, 'build')
else:
    build_path = os.path.join(THIS_DIR, 'build')
    if build_path not in os.environ['LD_LIBRARY_PATH']:
        os.environ['LD_LIBRARY_PATH'] += os.pathsep + build_path
