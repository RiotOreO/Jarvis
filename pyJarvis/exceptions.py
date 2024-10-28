# Jarvis - UserBot

"""
Exceptions which can be raised by py-Jarvis Itself.
"""


class pyJarvisError(Exception):
    ...


class DependencyMissingError(ImportError):
    ...


class RunningAsFunctionLibError(pyJarvisError):
    ...
