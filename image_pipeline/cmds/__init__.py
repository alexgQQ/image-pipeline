import os
from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

# Modify the import functionality a bit here to dynamically load files added to this module.
# The intent here is to collect all the Command instances and load them into a `commands` list
# for easy importing.

# Each file in this directory should have a single global click.core.Command class/function with
# the same name as its file

globals()['commands'] = []

package_dir = os.path.dirname(__file__)
for (_, module_name, _) in iter_modules([package_dir]):
    if module_name == 'utils':
        continue
    module = import_module(f"{__name__}.{module_name}")
    attribute = getattr(module, f'{module_name}_cmd')
    globals()['commands'].append(attribute)
