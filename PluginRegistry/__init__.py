import os
import logging
import traceback
from copy import copy
import sys
import importlib


class PluginRegistry(object):
    def __init__(self, registry_version="0.1"):
        self.__plugins = {}
        self.__enabled = {}
        self.__disabled = []
        self.__registry_version = registry_version

    def __getitem__(self, plugin_name):
        if plugin_name in self.__enabled.keys():
            return self.__enabled[plugin_name]
        return None

    def pluginClass(self, plugin_name):
        if plugin_name in self.__plugins.keys():
            return self.__plugins[plugin_name]
        return None

    def RegisterPlugin(self, plugin, prefix=""):
        if type(plugin) != str:
            logging.warning("Plugin must be a named string that exists in the Plugins directory")
            return

        logging.info("Registering plugin: " + plugin)

        if len(prefix) > 0 and not prefix.endswith('.'):
            prefix = prefix + '.'

        try:
            module = importlib.import_module(prefix + "Plugins." + plugin)
        except Exception as e:
            logging.exception("Nonexistent plugin module in Plugins/%s.py" % plugin)
            return

        try:
            plugin_class_name = str(module.__plugin__)
        except:
            logging.warning("No __plugin__ class name identifier in %s" % plugin)
            return

        try:
            plugin_class = getattr(module, plugin_class_name)
        except:
            logging.warning("Cannot obtain class named %s from module Plugins/%s.py" % (plugin_class_name, plugin))
            return

        registryVersion = self.__registry_version.split(".")

        try:
            moduleVersion = module.__plugin_version__.split(".")
        except:
            logging.warning("Cannot find plugin version for: " + plugin_class_name)
            return

        if moduleVersion[0] != registryVersion[0]:
            logging.warning("Module major version mismatch in Plugin: " + plugin_class_name)
            return

        for i in range(len(moduleVersion) - 1):
            regver = 0
            if i <= len(registryVersion) - 2:
                regver = registryVersion[i + 1]
            if moduleVersion[i + 1] > regver:
                logging.warning("Module %s is newer than registry" % plugin_class_name)
                return

        try:
            self.__plugins[plugin_class_name] = plugin_class
            logging.info("Plugin registered " + plugin_class_name)
        except Exception as e:
            logging.exception("Failed to register Plugin: " + plugin_class_name)

    def list(self):
        return copy(list(self.__plugins.keys()))

    def InitialisePlugins(self, params=None):
        for p in self.list():
            self.EnablePlugin(p, params)

    def LoadPlugins(self, path, prefix=""):
        sys.path.append(path)
        d = os.path.dirname(path)
        d = os.path.join(d, "Plugins")
        plugin_path = os.path.abspath(d)
        dirlist = os.listdir(plugin_path)
        for i in dirlist:
            if i.endswith("pyc"):
                continue
            if i == "__init__.py":
                continue
            if not i.endswith("py"):
                continue
            plugin = i.replace(".py", "")
            self.RegisterPlugin(plugin, prefix)

    def EnablePlugin(self, plugin, params=None):
        try:
            self.__enabled[plugin] = self.__plugins[plugin](**params)
        except:
            logging.debug(plugin)
            logging.exception("Loading plugin failed")

    def DisablePlugin(self, plugin):
        if plugin in self.__enabled.keys():
            del(self.__enabled[plugin])
        if plugin not in self.__disabled:
            self.__disabled.append(plugin)
