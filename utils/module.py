import sys
import types


def reload_modules(settings):
    if not settings.reload_modules:
        return

    import constants
    import utils
    import msfs_project
    import blender

    reload_package(constants)
    reload_package(utils)
    reload_package(msfs_project)
    reload_package(blender)

    from constants import EOL

    print("modules reloaded", EOL)


def reload_package(root_module):
    package_name = root_module.__name__

    # get a reference to each loaded module
    loaded_package_modules = dict([
        (key, value) for key, value in sys.modules.items()
        if key.startswith(package_name) and isinstance(value, types.ModuleType)])

    # delete references to these loaded modules from sys.modules
    for key in loaded_package_modules:
        del sys.modules[key]

    # load each of the modules again;
    # make old modules share state with new modules
    for key in loaded_package_modules:
        print("loading %s" % key)
        newmodule = __import__(key)
        oldmodule = loaded_package_modules[key]
        oldmodule.__dict__.clear()
        oldmodule.__dict__.update(newmodule.__dict__)
