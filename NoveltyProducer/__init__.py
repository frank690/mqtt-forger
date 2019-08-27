import os
import sys
import inspect
import pkgutil
from importlib import import_module

# make sure to add all dynamically created classes to the modules
# found at: https://www.bnmetrics.com/blog/dynamic-import-in-python3
for (_, name, _) in pkgutil.iter_modules([os.path.dirname(__file__)]):

    imported_module = import_module('.' + name, package=__name__)

    for i in dir(imported_module):
        attribute = getattr(imported_module, i)

        if inspect.isclass(attribute):
            setattr(sys.modules[__name__], name, attribute)