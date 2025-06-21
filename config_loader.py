# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2025-05-22
# modified: 2025-06-21
#
# This is a MicroPython-compatible simplified version of the ConfigLoader class
# used with the KROS robot operating system to load a YAML configuration file.
#
# Usage:
#
#     config = ConfigLoader.configure()   # defaults to 'config.yaml'
# or
#     config = ConfigLoader.configure('my_file.yaml')
#

import yaml

class ConfigLoader:

    DEFAULT_FILE = 'config.yaml'

    @staticmethod
    def configure(filename=None):
        path = filename or ConfigLoader.DEFAULT_FILE
        return yaml.load(path)
