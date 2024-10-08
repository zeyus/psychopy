#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import traceback
import yaml
import os
import sys
import codecs

from psychopy.localization import _translate


"""
The Alerts module is used for generating alerts during PsychoPy integrity checks.

Attributes
----------
catalog : AlertCatalog
    For loading alert catalogues, or definitions of each alert, from a catalog of yaml files.
    Each catalogue entry has a code key, with values of code, category, msg, and url.
    Each entry has equivalent reStructuredText entries for insertion into help pages. 
alertLog : List
    For storing alerts that are otherwise lost when flushing standard stream. The stored
    lists can be used to feed AlertPanel using in Project Info and new Runner frame.
"""

_activeAlertHandlers = []


class AlertCatalog:
    """A class for loading alerts from the alerts catalogue yaml file"""
    def __init__(self):
        self.alert = self.load()

    @property
    def alertPath(self):
        return Path(__file__).parent / "alertsCatalogue"

    @property
    def alertFiles(self):
        return list(self.alertPath.glob("*[0-9].*"))

    def load(self):
        """Loads alert catalogue yaml files

        Returns
        -------
        dict
            The alerts catalogue as a Python dictionary
        """
        alertDict = {}

        for filePath in self.alertFiles:
            # '{}'.format(filePath) instead of simple open(filePath,'r')
            # is needed for Py2 support only
            with codecs.open('{}'.format(filePath), 'r', 'utf-8') as ymlFile:
                entry = yaml.load(ymlFile, Loader=yaml.SafeLoader)
                if entry is None:
                    continue  # this might be a stub for future entry
                ID = entry['code']
                alertDict[ID] = entry
                if 'url' not in entry:  # give a default URL
                    entry['url'] = ('https://psychopy.org/alerts/{}.html'
                                    .format(ID))

        return alertDict


class AlertEntry:
    """An Alerts data class holding alert data as attributes

    Attributes
    ----------

    code: int
        The 4 digit code for retrieving alert from AlertCatalogue
    cat: str
        The category of the alert
    url: str
        A URL for pointing towards information resources for solving the issue
    obj: object
        The object related to the alert e.g., TextComponent object.
    type: str
        Type of component being tested
    name: str
        Name of component being tested
    msg: str
        The alert message
    trace: sys.exec_info() traceback object
            The traceback

    Parameters
    ----------
    code: int
            The 4 digit code for retrieving alert from AlertCatalogue
    obj: object
        The object related to the alert e.g., TextComponent object.
    strFields: dict
            Dict containing relevant values for formatting messages
    trace: sys.exec_info() traceback object
            The traceback
    """
    def __init__(self, code, obj, strFields=None, trace=None):
        self.label = catalog.alert[code]['label']
        self.code = catalog.alert[code]['code']
        self.cat = catalog.alert[code]['cat']
        self.url = catalog.alert[code]['url']
        self.obj = obj

        if hasattr(obj, 'type'):
            self.type = obj.type
        else:
            self.type = None

        if hasattr(obj, "params"):
            self.name = obj.params['name'].val
        else:
            self.name = None

        # _translate(catalog.alert[code]['msg']) works, but string literals
        # in _translate() (i.e., 'msg' in this case) cause false detection 
        # by pybabel.
        msg = catalog.alert[code]['msg']
        if strFields:
            self.msg = _translate(msg).format(**strFields)
        else:
            self.msg = _translate(msg)

        if trace:
            self.trace = ''.join(traceback.format_exception(
                trace[0], trace[1], trace[2]))
        else:
            self.trace = None


def alert(code=None, obj=object, strFields=None, trace=None):
    """The alert function is used for writing alerts to the standard error stream.
    Only the ErrorHandler class can receive alerts via the "receiveAlert" method.

    Parameters
    ----------
    code: int
        The 4 digit code for retrieving alert from AlertCatalogue
    obj: object
        The object related to the alert e.g., TextComponent object
    strFields: dict
        Dict containing relevant values for formatting messages
    trace: sys.exec_info() traceback object
            The traceback
    """

    msg = AlertEntry(code, obj, strFields, trace)

    # format the warning into a string for console and logging targets
    msgAsStr = ("Alert {code}: {msg}\n"
                "For more info see https://docs.psychopy.org/alerts/{code}.html"
                .format(type=msg.type,
                        name=msg.name,
                        code=msg.code,
                        cat=msg.cat,
                        msg=msg.msg,
                        trace=msg.trace))
    if len(_activeAlertHandlers):
        # if we have any active handlers, send to them
        for handler in _activeAlertHandlers:
            # send alert
            handler.receiveAlert(msg)
    elif hasattr(sys.stderr, 'receiveAlert'):
        # if there aren't any, but stdout can receive alerts, send to stdout
        sys.stderr.receiveAlert(msg)
    else:
        # otherwise, just write as a string to stdout
        sys.stderr.write(msgAsStr)


def isAlertHandler(handler):
    """
    Is the given handler an alert handler?

    Parameters
    ----------
    handler : ScriptOutputCtrl
        Handler to query.
    
    Returns
    -------
    bool
        True if the given handler is an alert handler.
    """
    return handler in _activeAlertHandlers


def addAlertHandler(handler):
    """
    Add a handler to the list of active alert handlers.

    Parameters
    ----------
    handler : ScriptOutputCtrl
        Handler to add.
    """
    if not isAlertHandler(handler):
        _activeAlertHandlers.append(handler)


def removeAlertHandler(handler):
    """
    Remove a handler from the list of active alert handlers.

    Parameters
    ----------
    handler : ScriptOutputCtrl
        Handler to remove.
    """
    if isAlertHandler(handler):
        _activeAlertHandlers.pop(
            _activeAlertHandlers.index(handler)
        )


# Create catalog
catalog = AlertCatalog()
alertLog = []
