#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Library of issues that the user might encounter, our own form of error
handling

"""

#  Part of the PsychoPy library
# Copyright (C) 2018 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).


import os
issues = {}
from .base import Issue

def getIssue(code):
    return issues[code]

import glob
import importlib

_issuesFolder = os.path.split(__file__)[0]
_issueFiles = glob.glob(os.path.join(_issuesFolder, "issue*.py"))
_issueFiles.sort()
for _thisFile in _issueFiles:
    _modName = '.'+os.path.split(_thisFile)[1][:-3]
    try:
        mod = importlib.import_module(_modName, package='psychopy.issues')
    except ImportError:
        continue
    issues[mod.code] = Issue(mod.code, mod.descr, mod.help)

