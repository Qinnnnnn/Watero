#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
File : pip_upgrade.py
Author : Zerui Qin
CreateDate : 2019-04-25 15:04:41 
Note : pip批量更新
"""

from subprocess import call

from pip._internal.utils.misc import get_installed_distributions

for dist in get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)
