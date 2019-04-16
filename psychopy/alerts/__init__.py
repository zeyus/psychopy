#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Library of issues that the user might encounter, our own form of error
handling

"""

#  Part of the PsychoPy library
# Copyright (C) 2018 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).


import os
import glob
import importlib
from .base import Alert

knownAlerts = None


def raiseAlert(code, obj=None):
    """Function to raise a new alert with a given code and, optionally, the
    object to which the alert refers"""
    global knownAlerts
    if not knownAlerts:
        knownAlerts = getKnownAlerts()
    return knownAlerts[code]


def getKnownAlerts():
    """Checks the alerts files and creates a dictionary to act as a catalog of
    avalailable alerts. This is generally done

    Returns
    -------

    """
    alerts={}
    _alertsFolder = os.path.split(__file__)[0]
    _alertsFiles = glob.glob(os.path.join(_alertsFolder, "issue*.py"))
    _alertsFiles.sort()
    for _thisFile in _alertsFiles:
        _modName = '.'+os.path.split(_thisFile)[1][:-3]
        try:
            mod = importlib.import_module(_modName, package='psychopy.issues')
        except ImportError:
            continue
        alerts[mod.code] = Alert(mod.code, mod.descr, mod.help)

